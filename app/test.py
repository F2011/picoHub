from matplotlib import pyplot as plt
from PIL import Image


w = 296
h = 152
w_pixel = 0.0202
h_pixel = 0.0203
w_fig = round((w * w_pixel) * 0.39, 4)
h_fig = round((h * h_pixel) * 0.39, 4)

def create_image(tex: str) -> Image:
    image_name = "tmp/pict.jpg"
    plt.rcParams.update({
        # "text.usetex": True,
        "font.family": "monospace",
        "font.sans-serif": "Helvetica",
    })

    fig = plt.figure(figsize=(w_fig, h_fig), linewidth=1, edgecolor='black', dpi=int(w / w_fig), frameon=False)
    fig.text(0, 0, tex, wrap=True, ha="left")
    plt.savefig(image_name, bbox_inches='tight', pad_inches=0)
    img = Image.open(image_name) # open colour image
    return img.convert('1', dither=Image.NONE) # convert image to black and white

def create_bitlist(img: Image) -> list[int]:
    bitlist = []
    buf = img.getdata()
    for i in range(0, img.size[1]):
        bitlist.append(buf[i*img.size[0]:(i+1)*img.size[0]])
    for b_array in bitlist:
        b_array.extend([0 for _ in range(w - img.size[0])])
        # do something here
        #
        #
        #
        # for _ in range(w - img.size[0]):
        #     bitlist.insert(y * w + img.size[0], 0)
    bitlist.extend([0 for _ in range((h - img.size[1]) * w)])
    return bitlist


if __name__ == "__main__":
    tex = "The value of the expression $[(2^{1004}+5^{1005})^2-(2^{1004}-5^{1005})^2]$ is $k\\cdot10^{1004}$ for some positive integer $k$. What is $k$?"
    img = create_image(tex)
    bitlist = create_bitlist(img)

    print(len(img.getdata()), img.size[0], img.size[1], img.size[0]*img.size[1])
    print(len(bitlist), len(bitlist) / w, h)
    for i in img.getdata():
        print(i, end=" ")
