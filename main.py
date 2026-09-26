from scraping import scraping_codeforce
from data_analysis import analyze_codeforces

def main():
    print("Codeforceのスクレイピングを開始します")
    scraping_codeforce()

    print("集めたデータの分析とレポート作成を行います")
    analyze_codeforces()
    print("レポート作成が完了しました")

if __name__ == "__main__":
    main()
