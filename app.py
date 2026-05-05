import streamlit as st
from PIL import Image
import io

st.title("タップで変わる！X（Twitter）完全最適化版🖤")
st.write("2000pxでも綺麗に消える、アンチエイリアス完全排除モデルなのだ。")

# 輝度調整のスライダー（ここが成功の鍵かも）
brightness = st.sidebar.slider("下絵の明るさ補正 (低いほどプレビューで隠れる)", 0.1, 1.0, 0.7)

col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：常に表示する透過PNG", type=["png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    # サイズは2000px程度を維持（1枚目に合わせる）
    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.NEAREST)

    output_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    for y in range(height):
        for x in range(width):
            r2, g2, b2, a2 = pixels2[x, y]
            
            # 2枚目の絵を優先（アンチエイリアスを消すため閾値を高めに）
            if a2 > 150:
                output_pixels[x, y] = (r2, g2, b2, 255)
            else:
                # 1ピクセルごとの完全な市松模様
                if (x + y) % 2 == 0:
                    r1, g1, b1, a1 = pixels1[x, y]
                    # 下絵を少し暗くして背景に馴染ませる[cite: 2]
                    output_pixels[x, y] = (int(r1 * brightness), int(g1 * brightness), int(b1 * brightness), 255)
                else:
                    # 完全に透明
                    output_pixels[x, y] = (0, 0, 0, 0)

    # ★重要：ディザリングなしで減色してパレット画像にする
    # dither=Image.Dither.NONE を指定して中間色を一切作らせない[cite: 2]
    quantized_image = output_image.convert("P", palette=Image.Palette.ADAPTIVE, colors=256, dither=Image.Dither.NONE)

    st.image(quantized_image, caption="2000pxでもパキパキなのだ🖤", use_container_width=True)

    buf = io.BytesIO()
    # 透過PNGとして保存。これならXのプレビューを騙せるはず。[cite: 2]
    quantized_image.save(buf, format="PNG", optimize=True)
    st.download_button(
        label="X（Twitter）向けに保存する",
        data=buf.getvalue(),
        file_name="x_optimized_tap.png",
        mime="image/png"
    )
else:
    st.info("成功例に近づけるには、左の明るさ補正を少し下げてみてね。")