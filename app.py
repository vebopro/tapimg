import streamlit as st
from PIL import Image
import io

st.title("タップで変わる画像作成ツール🖤")
st.write("2000ピクセル以上、1枚目と2枚目は同じ縦横サイズにしてね。")

col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像（JPG/PNG）", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：上に重ねる透過PNG", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.LANCZOS)

    # 結果用の透明キャンバス
    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    # 合成ロジック（さっきと同じ）
    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            if a2 > 0:
                output_pixels[x, y] = (r2, g2, b2, a2)
            else:
                if (x + y) % 2 == 0:
                    output_pixels[x, y] = pixels1[x, y]
                else:
                    output_pixels[x, y] = (0, 0, 0, 0)

    # ★ここが追加部分なのだ★
    # RGBA画像を256色のインデックスカラー（8ビット）に減色する
    quantized_image = output_image.quantize(colors=256)

    # 画面には減色後のものを表示
    st.image(quantized_image, caption="合成完了なのだ🖤", use_container_width=True)

    # ダウンロード（保存も8ビットPNGになるよ）
    buf = io.BytesIO()
    quantized_image.save(buf, format="PNG")
    st.download_button(
        label="8ビット合成画像を保存する",
        data=buf.getvalue(),
        file_name="8bit_tap_reveal.png",
        mime="image/png"
    )
else:
    st.info("画像を2枚アップロードしてね。最後は自動で8ビット化されるのだ( ˙-˙ )")