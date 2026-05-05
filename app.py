import streamlit as st
from PIL import Image
import io

st.title("ピクセル透過ツール??")
st.write("画像をアップすると、1ピクセルごとに格子状に透過するのだ。")

# ファイルアップローダー
uploaded_file = st.file_uploader("画像を選んでね", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 画像を開く
    input_image = Image.open(uploaded_file).convert("RGBA")
    pixels = input_image.load()
    width, height = input_image.size

    # 透過処理
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 1:
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)

    # 結果の表示
    st.image(input_image, caption="変換後のイメージなのだ", use_container_width=True)

    # ダウンロードボタン
    buf = io.BytesIO()
    input_image.save(buf, format="PNG")
    st.download_button(
        label="画像を保存する",
        data=buf.getvalue(),
        file_name="transparent_checker.png",
        mime="image/png"
    )