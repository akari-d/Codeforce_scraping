import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

def analyze_codeforces():
    df = pd.read_csv("codeforces_problems.csv")
    copy_df = df.copy()

    #1 難易度別の平均回答数の集計
    difficulty_level = df.groupby("rating")["solved_count"].mean().round(2).sort_values(ascending=False)
    #print(difficulty_level)

    rating_mean = df["rating"].mean().round(2)
    rating_median = df["rating"].median().round(2)
    rating_max = df["rating"].max().round(2)
    rating_min = df["rating"].min().round(2)

    #tag別
    copy_df["tags"] = copy_df["tags"].str.split(", ")
    copy_df = copy_df.explode("tags")
    copy_df = copy_df.rename(columns={"tags": "tag"})

    tag_count = copy_df.groupby("tag")["solved_count"].sum().sort_values(ascending=False).reset_index()

    tag_rating_mean = copy_df.groupby("tag")["rating"].mean().round(1).sort_values(ascending=False).reset_index()

    #回答数　ベスト１０
    df = df.sort_values("solved_count", ascending=False)
    df["rank"] = df["solved_count"].rank(
        method="min",
        ascending=False
    ).astype(int)

    #初心者おすすめ問題
    beginner_problem = df[(df["rating"] <= 1000) & (df["solved_count"] >= 10000)]
    #print(beginner_problem[["problem_id", "title", "rating", "solved_count", "url"]])

    #初心者向けをCSVファイルに出力
    beginner_problem.to_csv("beginner_problems.csv", index=False)

    #グラフの作成
    japanize_matplotlib.japanize()
    #最も解かれた問題の上位10件を棒グラフで表示
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = df["title"].head(10)
    y_positions = range(len(labels))
    values = df["rank"].head(10)

    ax.barh(y_positions, values, tick_label=labels)
    ax.set_xlabel("Rank")
    ax.set_ylabel("Problem Title")
    ax.set_title("最も解かれた問題の上位10件")
    fig.tight_layout()
    plt.savefig('problem_top10.png', dpi=300)
    plt.close()


    #どの難易度の問題が多いか、ヒストグラムで表示
    fig, ax = plt.subplots(figsize=(10, 6))
    bins = [800,1200,1600,2000,2400,2800,3200,3600]
    ax.hist(df["rating"].dropna(), bins=bins)
    ax.set_xlabel("rating")
    ax.set_ylabel("Problem Count")
    ax.set_title("難易度別の問題数")
    fig.tight_layout()
    plt.savefig('rating_ploblem_count.png', dpi=300)
    plt.close()

    #tagの出現数　TOP10
    fig, ax = plt.subplots(figsize=(10, 6))
    tag_counts = copy_df["tag"].value_counts().head(10)

    ax.barh(tag_counts.index, tag_counts.values)
    ax.set_xlabel("Count")
    ax.set_ylabel("Tag")
    ax.set_title("tagの出現数 Top 10")
    fig.tight_layout()
    plt.savefig('tag_count.png', dpi=300)
    plt.close()

    #tag別の平均難易度　TOP10
    fig, ax = plt.subplots(figsize=(10, 6))
    tag_rating_mean = tag_rating_mean.head(10)
    ax.barh(tag_rating_mean["tag"], tag_rating_mean["rating"])
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Tag")
    ax.set_title("tag別の平均難易度 Top 10")
    fig.tight_layout()
    plt.savefig('tag_rating_mean.png', dpi=300)
    plt.close()

    #solved_countとratingの関係を散布図で表示
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["rating"], df["solved_count"])
    ax.set_xlabel("rating")
    ax.set_ylabel("solved_count")
    ax.set_title("solved_countとratingの関係")
    fig.tight_layout()
    plt.savefig('scatter.png', dpi=300)
    plt.close()

    report = f"""
        # Codeforce分析レポート

        ## データ概要
        取得問題数:{len(df)}件
        Ratingの平均:{rating_mean:.1f}
        Ratingの中央値:{rating_median:.1f}
        Ratingの最大値:{rating_max:.1f}
        Ratingの最小値:{rating_min:.1f}

        #人気問題TOP10
        {df[["rank", "title", "solved_count"]].head(10).to_string(index= False)}

        #初心者向け問題 5選
        {beginner_problem[["problem_id","title"]].head(5).to_string(index= False)}

        #タグ別・対象問題のsolved_count合計 TOP10
        {tag_count.dropna().head(10).to_string(index= False)}

        #tag別の平均難易度
        {tag_rating_mean.dropna().head(10).to_string(index= False)}
    """
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)

