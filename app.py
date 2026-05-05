import streamlit as st
from PIL import Image
import io

st.title("タップで変わる！ガチ勢向けツール🖤")
st.write("アンチエイリアスを排除して、SNSの圧縮を逆手に取る設定なのだ。")

# 設定[cite: 1, 2]
st.sidebar.header("詳細設定")
density = st.sidebar.slider("ドットの間隔 (大きいほど隠し絵が薄くなる)", 2, 8, 2)
# 1/density の確率でドットを残す仕組みにするのだ

col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：常に表示する透過PNG", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # 画像読み込み
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    # ★重要：リサイズは必ず NEAREST（Nearest Neighbor）を使うのだ
    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.NEAREST)

    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    # 合成ロジック
    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            # 2枚目に絵がある（不透明）なら優先
            if a2 > 128: # 念のため中間的な透過もカット
                output_pixels[x, y] = (r2, g2, b2, 255)
            else:
                # 1枚目をドット状に配置[cite: 2]
                if (x % density == 0) and (y % density == 0):
                    output_pixels[x, y] = pixels1[x, y]
                else:
                    output_pixels[x, y] = (0, 0, 0, 0)

    # インデックス256色化（8ビット透過PNG用）
    # 自前でパレット制御するのは大変だから、最良のアルゴリズムで減色
    quantized_image = output_image.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)

    st.image(quantized_image, caption="合成完了（Nearest補正済み）なのだ🖤", use_container_width=True)

    buf = io.BytesIO()
    # 透過情報を維持して保存
    quantized_image.save(buf, format="PNG", optimize=True)
    st.download_button(
        label="ガチ仕様で保存する",
        data=buf.getvalue(),
        file_name="tap_reveal_strict.png",
        mime="image/png"
    )
else:
    st.info("チュートリアル通り、高解像度の画像を使うとさらに成功率が上がるよ。")