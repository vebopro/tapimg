import streamlit as st
from PIL import Image
import io

st.title("タップで変わる！合成ツール🖤")
st.write("1枚目を格子状に透過させて、その上に2枚目の透過PNGを重ねるのだ。")

# アップローダーの設定
col1, col2 = st.columns(2)
with col1:
    # 1枚目は何でもOK
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像", type=["png", "jpg", "jpeg"])
with col2:
    # 2枚目は透過PNG限定[cite: 1]
    uploaded_file2 = st.file_uploader("2枚目：上に重ねる透過PNG", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # 画像を読み込んでRGBAに変換
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    # 1枚目のサイズに2枚目を合わせる[cite: 2]
    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.LANCZOS)

    # 1. 1枚目（隠し画像）に格子状の穴をあける[cite: 2]
    pixels1 = img1.load()
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 1:
                r, g, b, a = pixels1[x, y]
                pixels1[x, y] = (r, g, b, 0) # 透明にする

    # 2. 加工した1枚目の上に、2枚目をそのまま重ねる[cite: 2]
    # alpha_compositeを使うことで、2枚目の不透明な部分はそのまま残るのだ
    combined_image = Image.alpha_composite(img1, img2)

    # 結果の表示
    st.image(combined_image, caption="合成完了なのだ🖤", use_container_width=True)

    # ダウンロード
    buf = io.BytesIO()
    combined_image.save(buf, format="PNG")
    st.download_button(
        label="合成画像を保存する",
        data=buf.getvalue(),
        file_name="tap_to_reveal.png",
        mime="image/png"
    )
else:
    st.info("画像を2枚アップロードしてね。2枚目は透過PNGじゃないとダメなのだ( ˙-˙ )")