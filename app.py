import streamlit as st
from PIL import Image
import io

st.title("タップで変わる画像作成🖤")
st.write("2000ピクセル以上、1枚目と2枚目は同じサイズにしてね。")

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

    # 合成ロジック[cite: 2]
    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            if a2 > 0:
                # 2枚目の絵がある場所（不透明な場所）は、2枚目をそのまま描画（1枚目を上書き）
                output_pixels[x, y] = (r2, g2, b2, a2)
            else:
                # 2枚目が透明な場所だけ、格子処理を行う
                if (x + y) % 2 == 0:
                    # 偶数ピクセルは1枚目
                    output_pixels[x, y] = pixels1[x, y]
                else:
                    # 奇数ピクセルは透明（背景色に依存させるため）
                    output_pixels[x, y] = (0, 0, 0, 0)

    st.image(output_image, caption="合成完了なのだ🖤", use_container_width=True)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    st.download_button(
        label="合成画像を保存する",
        data=buf.getvalue(),
        file_name="perfect_tap_reveal.png",
        mime="image/png"
    )
else:
    st.info("合成完了なのだ🖤")