import streamlit as st
from PIL import Image
import io

st.title("タップで変わる！ドット極小版🖤")

# densityを2にすると今の「デカい格子」になるから、1固定か細かい調整にする
# 解像度ブースト機能を追加
upscale = st.sidebar.checkbox("解像度を2倍にしてドットを細かくする", value=True)

col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：常に表示する透過PNG", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    # もし画像が小さいなら強制的に拡大してドットを細かく見せる
    if upscale:
        new_size = (img1.width * 2, img1.height * 2)
        img1 = img1.resize(new_size, Image.Resampling.NEAREST)
    
    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.NEAREST)

    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            if a2 > 128:
                output_pixels[x, y] = (r2, g2, b2, 255)
            else:
                # 最小単位（1ピクセル）で交互に配置する
                if (x + y) % 2 == 0:
                    output_pixels[x, y] = pixels1[x, y]
                else:
                    output_pixels[x, y] = (0, 0, 0, 0)

    # 8ビット化
    quantized_image = output_image.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)

    st.image(quantized_image, caption="ドットを極限まで細かくしたのだ🖤", use_container_width=True)

    buf = io.BytesIO()
    quantized_image.save(buf, format="PNG", optimize=True)
    st.download_button(
        label="極小ドット版を保存する",
        data=buf.getvalue(),
        file_name="ultra_fine_dot.png",
        mime="image/png"
    )