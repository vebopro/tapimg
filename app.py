import streamlit as st
from PIL import Image
import io

st.title("タップで変わる画像作成ツール🖤")
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

    # まっさらな透明キャンバスを作る
    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    # 1ピクセルずつ交互に埋めるロジック[cite: 2]
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                # 偶数ピクセルは1枚目（隠し画像）
                output_pixels[x, y] = pixels1[x, y]
            else:
                # 奇数ピクセルは2枚目（透過PNG）
                # 2枚目の透過部分はそのまま透過になる
                output_pixels[x, y] = pixels2[x, y]

    st.image(output_image, caption="合成完了なのだ🖤", use_container_width=True)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    st.download_button(
        label="合成画像を保存する",
        data=buf.getvalue(),
        file_name="checker_tap_image.png",
        mime="image/png"
    )
else:
    st.info("合成完了なのだ🖤")