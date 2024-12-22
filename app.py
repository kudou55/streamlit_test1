import streamlit as st  
import pandas as pd  
import matplotlib.pyplot as plt  
import seaborn as sns  
import matplotlib.font_manager as fm  
import os  
  
def set_japanese_font():  
    """  
    ローカルに保存されたNoto Sans JPフォントをMatplotlibに設定します。  
    """  
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "NotoSansJP-Regular.otf")  
    if os.path.exists(font_path):  
        try:  
            fm.fontManager.addfont(font_path)  
            plt.rcParams['font.family'] = 'Noto Sans JP'  
            plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の表示設定  
        except Exception as e:  
            st.error(f"フォントの設定中にエラーが発生しました: {e}")  
    else:  
        st.error("フォントファイルが見つかりません。'fonts' フォルダに 'NotoSansJP-Regular.otf' を配置してください。")  
  
def main():  
    set_japanese_font()  
      
    st.set_page_config(page_title="CSVファイル分析ダッシュボード", layout="wide")  
    st.title("CSVファイル分析ダッシュボード")  
    st.write("CSVファイルをアップロードしてデータを分析しましょう。")  
      
    uploaded_file = st.file_uploader("CSVファイルを選択してください", type=["csv"])  
      
    if uploaded_file is not None:  
        try:  
            df = pd.read_csv(uploaded_file)  
            st.subheader("データプレビュー")  
            st.dataframe(df)  
      
            st.subheader("基本統計量")  
            st.write(df.describe())  
      
            # サイドバーにグラフの種類選択オプションを追加  
            st.sidebar.header("グラフ設定")  
      
            # 数値列の選択  
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns  
            if len(numeric_columns) > 0:  
                st.subheader("相関マトリックス")  
                  
                # 数値列の分散がゼロでないもののみを選択  
                numeric_df = df[numeric_columns].dropna()  # 欠損値を含む行を削除  
                numeric_df = numeric_df.loc[:, numeric_df.var() != 0]  # 分散がゼロの列を除外  
                  
                if numeric_df.shape[1] < 2:  
                    st.warning("クラスタマップの作成には少なくとも2つ以上の数値列が必要です。")  
                else:  
                    corr_plot_type = st.sidebar.selectbox(  
                        "相関マトリックスの表示形式",  
                        ("ヒートマップ", "クラスタマップ")  
                    )  
                    corr = numeric_df.corr()  
                      
                    # 相関マトリックスが空でないかを確認  
                    if corr.empty or corr.shape[0] == 0:  
                        st.warning("相関マトリックスが空です。データを確認してください。")  
                    else:  
                        if corr_plot_type == "ヒートマップ":  
                            fig, ax = plt.subplots(figsize=(10, 8))  
                            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt=".2f")  
                            st.pyplot(fig)  
                        elif corr_plot_type == "クラスタマップ":  
                            try:  
                                sns.clustermap(corr, annot=True, cmap='coolwarm', fmt=".2f")  
                                st.pyplot()  
                            except ValueError as ve:  
                                st.error(f"クラスタマップの作成中にエラーが発生しました: {ve}")  
      
                st.subheader("ペアプロット")  
                pairplot_type = st.sidebar.selectbox(  
                    "ペアプロットのスタイル",  
                    ("Seaborn", "Matplotlib")  
                )  
                if pairplot_type == "Seaborn":  
                    if numeric_df.shape[1] < 2:  
                        st.warning("ペアプロットの作成には少なくとも2つ以上の数値列が必要です。")  
                    else:  
                        pair_fig = sns.pairplot(numeric_df)  
                        st.pyplot(pair_fig)  
                else:  
                    if numeric_df.shape[1] < 2:  
                        st.warning("散布図行列の作成には少なくとも2つ以上の数値列が必要です。")  
                    else:  
                        fig2, ax2 = plt.subplots(figsize=(12, 12))  
                        pd.plotting.scatter_matrix(numeric_df, ax=ax2, figsize=(12, 12))  
                        st.pyplot(fig2)  
      
            else:  
                st.write("数値データが含まれていません。")  
      
            # カテゴリカルデータの分析  
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns  
            if len(categorical_columns) > 0:  
                st.subheader("カテゴリカルデータの分布")  
                for col in categorical_columns:  
                    st.write(f"**{col}**")  
                    plot_type = st.sidebar.selectbox(  
                        f"{col} のプロットタイプ",  
                        ("カウントプロット", "バープロット", "パイチャート"),  
                        key=col  
                    )  
                    fig, ax = plt.subplots(figsize=(8, 6))  
                    if plot_type == "カウントプロット":  
                        sns.countplot(data=df, x=col, ax=ax)  
                        plt.xticks(rotation=45)  
                    elif plot_type == "バープロット":  
                        counts = df[col].value_counts()  
                        sns.barplot(x=counts.index, y=counts.values, ax=ax)  
                        plt.xticks(rotation=45)  
                    elif plot_type == "パイチャート":  
                        counts = df[col].value_counts()  
                        ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=140)  
                        ax.axis('equal')  
                    st.pyplot(fig)  
        except Exception as e:  
            st.error(f"エラーが発生しました: {e}")  
    else:  
        st.info("左上のボタンからCSVファイルをアップロードしてください。")  
  
if __name__ == "__main__":  
    main()  