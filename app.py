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

    # ====================== おすすめ設定 ======================
    HIDDEN_STRENGTH = 0.28   # 0.20〜0.35の間で調整してください
    # =========================================================

    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            if a2 > 10:  # 2枚目の不透明部分をしっかり優先
                output_pixels[x, y] = (r2, g2, b2, a2)
            else:
                if (x + y) % 2 == 0:                    # チェッカーボード
                    r1, g1, b1, a1 = pixels1[x, y]
                    hidden_a = int(a1 * HIDDEN_STRENGTH)
                    output_pixels[x, y] = (r1, g1, b1, hidden_a)
                else:
                    output_pixels[x, y] = (0, 0, 0, 0)

    # 256色に減色（dithering強化）
    quantized_image = output_image.quantize(colors=256, method=2)

    # 画面表示
    st.image(quantized_image, caption="合成完了なのだ🖤", use_container_width=True)

    # ダウンロード
    buf = io.BytesIO()
    quantized_image.save(buf, format="PNG", optimize=True)
    st.download_button(
        label="8ビット合成画像を保存する",
        data=buf.getvalue(),
        file_name="8bit_tap_reveal.png",
        mime="image/png"
    )

else:
    st.info("画像を2枚アップロードしてね。最後は自動で8ビット化されるのだ( ˙-˙ )")