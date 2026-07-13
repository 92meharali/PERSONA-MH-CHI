"""Part 12 — Clustering response archetypes."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.clustering")

FEATURES = ["HuMT", "E", "D", "F", "OA"]


def run_clustering(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "clustering"
    out_fig = cfg.figures_dir / "clustering"
    out_tab = cfg.tables_dir / "clustering"

    data = df[FEATURES + ["model", "dataset_family", "prompt_id"]].dropna().copy()
    scaler = StandardScaler()
    X = scaler.fit_transform(data[FEATURES])

    # Choose k by silhouette for kmeans
    sil_rows = []
    best_k, best_score = 2, -1.0
    for k in range(2, 8):
        km = KMeans(n_clusters=k, random_state=cfg.random_seed, n_init=10)
        labels = km.fit_predict(X)
        score = float(silhouette_score(X, labels))
        sil_rows.append({"k": k, "silhouette": score})
        if score > best_score:
            best_k, best_score = k, score
    sil = pd.DataFrame(sil_rows)
    save_csv(sil, out_res / "kmeans_silhouette.csv")

    kmeans = KMeans(n_clusters=best_k, random_state=cfg.random_seed, n_init=10)
    data["cluster_kmeans"] = kmeans.fit_predict(X)

    agg = AgglomerativeClustering(n_clusters=best_k)
    data["cluster_hierarchical"] = agg.fit_predict(X)

    db = DBSCAN(eps=1.2, min_samples=8)
    data["cluster_dbscan"] = db.fit_predict(X)

    # PCA / projection for viz (UMAP optional)
    pca = PCA(n_components=2, random_state=cfg.random_seed)
    pcs = pca.fit_transform(X)
    data["pc1"], data["pc2"] = pcs[:, 0], pcs[:, 1]

    try:
        import umap

        reducer = umap.UMAP(random_state=cfg.random_seed, n_neighbors=15, min_dist=0.1)
        emb = reducer.fit_transform(X)
        data["umap1"], data["umap2"] = emb[:, 0], emb[:, 1]
        has_umap = True
    except Exception as exc:
        logger.warning("UMAP unavailable (%s); using PCA only.", exc)
        data["umap1"], data["umap2"] = data["pc1"], data["pc2"]
        has_umap = False

    save_csv(data[["prompt_id", "model", "dataset_family", *FEATURES,
                   "cluster_kmeans", "cluster_hierarchical", "cluster_dbscan",
                   "pc1", "pc2", "umap1", "umap2"]],
             out_res / "cluster_assignments.csv")

    centers = data.groupby("cluster_kmeans")[FEATURES].mean().reset_index()
    save_csv(centers, out_res / "kmeans_centers.csv")
    dataframe_to_latex(centers, out_tab / "kmeans_centers.tex",
                       caption="KMeans cluster centroids in PERSONA space.",
                       label="tab:clusters")

    # Figures
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sc = ax.scatter(data["pc1"], data["pc2"], c=data["cluster_kmeans"], cmap="tab10", s=12, alpha=0.7)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title(f"KMeans clusters (k={best_k}) in PCA space")
    fig.colorbar(sc, ax=ax, fraction=0.046)
    save_fig(fig, out_fig / "fig_clusters_pca.png", dpi=cfg.dpi)

    if has_umap:
        fig, ax = plt.subplots(figsize=(6.5, 5))
        sc = ax.scatter(data["umap1"], data["umap2"], c=data["cluster_kmeans"], cmap="tab10", s=12, alpha=0.7)
        ax.set_xlabel("UMAP1")
        ax.set_ylabel("UMAP2")
        ax.set_title("KMeans clusters in UMAP space")
        fig.colorbar(sc, ax=ax, fraction=0.046)
        save_fig(fig, out_fig / "fig_clusters_umap.png", dpi=cfg.dpi)

    # Dendrogram on subsample
    sample = X[np.random.default_rng(cfg.random_seed).choice(len(X), size=min(120, len(X)), replace=False)]
    Z = linkage(sample, method="ward")
    fig, ax = plt.subplots(figsize=(10, 4))
    dendrogram(Z, ax=ax, no_labels=True)
    ax.set_title("Hierarchical clustering dendrogram (subsample)")
    save_fig(fig, out_fig / "fig_dendrogram.png", dpi=cfg.dpi)

    save_json({"best_k": best_k, "best_silhouette": best_score, "has_umap": has_umap},
              out_res / "clustering_summary.json")
    logger.info("Part 12 clustering complete (k=%d).", best_k)
    return {"assignments": data, "centers": centers, "best_k": best_k}
