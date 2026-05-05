import streamlit as st
from PIL import Image
import io

st.title("タップで変わる合成ツール")
st.write("1枚目（隠れる画像）と2枚目（見える画像）を交互に混ぜて合成するのだ。2000px以上の大きさにして、２枚とも大きさを揃えてね")

# 2つのファイルアップローダー[cite: 1]
col1, col2 = st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("1枚目：隠したい画像", type=["png", "jpg", "jpeg"])
with col2:
    uploaded_file2 = st.file_uploader("2枚目：常に表示する画像 透過PNGにしてね", type=["png", "jpg", "jpeg"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # 画像を開く[cite: 2]
    img1 = Image.open(uploaded_file1).convert("RGBA")
    img2 = Image.open(uploaded_file2).convert("RGBA")

    # 1枚目のサイズに2枚目を合わせる[cite: 2]
    width, height = img1.size
    img2 = img2.resize((width, height), Image.Resampling.LANCZOS)

    # 新しい画像を作成
    output_image = Image.new("RGBA", (width, height))
    pixels1 = img1.load()
    pixels2 = img2.load()
    output_pixels = output_image.load()

    # 交互にピクセルを合成するロジック[cite: 2]
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                # 偶数ピクセルは1枚目
                output_pixels[x, y] = pixels1[x, y]
            else:
                # 奇数ピクセルは2枚目
                output_pixels[x, y] = pixels2[x, y]

    # 結果の表示
    st.image(output_image, caption="合成完了なのだ", use_container_width=True)

    # ダウンロードボタン
    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    st.download_button(
        label="合成画像を保存する",
        data=buf.getvalue(),
        file_name="combined_image.png",
        mime="image/png"
    )
else:
    st.info("画像を2枚ともアップロードしてほしいのだ")