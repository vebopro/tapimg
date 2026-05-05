import streamlit as st
from PIL import Image
import io

st.title("タップで変わる画像作成ツール🖤")
st.write("2000ピクセル以上、1枚目と2枚目は同じ縦横サイズにしてね。")

col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像（Base）", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：上に重ねる透過PNG（Tap Layer）", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # 画像読み込み
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.LANCZOS)

    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    # ==================== 成功例に近い処理 ====================
    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            if a2 > 5:  # 2枚目の不透明部分を優先
                output_pixels[x, y] = (r2, g2, b2, a2)
            else:
                # 1px市松模様で極端に間引く（これが重要！）
                if (x % 2 == 0) and (y % 2 == 0):   # 1px checkerboard（25%だけ残す）
                    r1, g1, b1, a1 = pixels1[x, y]
                    # alphaをかなり低く（バレにくくするため）
                    hidden_a = int(a1 * 0.18) if a1 > 0 else 0
                    output_pixels[x, y] = (r1, g1, b1, hidden_a)
                else:
                    output_pixels[x, y] = (0, 0, 0, 0)
    # =======================================================

    # PNG-8（256色）に変換（ditheringを強く）
    quantized_image = output_image.quantize(
        colors=256, 
        method=2,      # dithering強化
        dither=1       # Floyd-Steinberg dither
    )

    st.image(quantized_image, caption="合成完了なのだ🖤", use_container_width=True)

    # ダウンロード
    buf = io.BytesIO()
    quantized_image.save(buf, format="PNG", optimize=True)
    st.download_button(
        label="8ビット合成画像を保存する",
        data=buf.getvalue(),
        file_name="tap_reveal.png",
        mime="image/png"
    )

else:
    st.info("画像を2枚アップロードしてね。最後は自動で8ビット化されるのだ( ˙-˙ )")