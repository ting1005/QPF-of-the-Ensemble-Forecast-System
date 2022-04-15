import numpy as np


def nws_precip_colors():
    nan_zero = [
        "#FFFFFF",  # nan
        "#FFFFFF"  # 0.00
    ]

    nws_precip_colors_original = [
        # "#FFFFFF",
        "#F0F0F0",
        "#9BFFFF",  # 0.01 2
        "#00CFFF",  # 5.00 6
        "#0198FF",  # 10.00 10
        "#0615FF",  # Blue 15
        "#3CBF01",  # 20.00 20
        "#65FF40",  # 25.00 30
        "#FFFF40",  # 30.00 40
        "#FFCB00",  # 35.00 50
        # "#FF9A00",  # 40.00 70
        "#FA0300",  # 45.00 90
        "#CC0003",  # 50.00 110
        "#A00000",  # 55.00 130
        "#98009A",  # 60.00 150
        "#C304CC",  # 65.00 200
        "#F805F3",  # 65.00 300
        "#FECBFF",  # 65.00 400
    ]

    # In [5]:
    # nws_precip_colors = [
    #     "#04e9e7",  # 0.01 - 0.10 inches
    #     "#019ff4",  # 0.10 - 0.25 inches
    #     "#0300f4",  # 0.25 - 0.50 inches
    #     "#02fd02",  # 0.50 - 0.75 inches
    #     "#01c501",  # 0.75 - 1.00 inches
    #     "#008e00",  # 1.00 - 1.50 inches
    #     "#fdf802",  # 1.50 - 2.00 inches
    #     "#e5bc00",  # 2.00 - 2.50 inches
    #     "#fd9500",  # 2.50 - 3.00 inches
    #     "#fd0000",  # 3.00 - 4.00 inches
    #     "#d40000",  # 4.00 - 5.00 inches
    #     "#bc0000",  # 5.00 - 6.00 inches
    #     "#f800fd",  # 6.00 - 8.00 inches
    #     "#9854c6",  # 8.00 - 10.00 inches
    #     "#fdfdfd"   # 10.00+
    # ]
    color_int = []
    # print("show i==1 ")
    # print(np.linspace(int(nws_precip_colors_original[1][1:3], 16), int(nws_precip_colors_original[1+1][1:3], 16), 500))
    for i, val in enumerate(nws_precip_colors_original[:-1]):
        # print("i=",i," val=",val)
        red = [val for val in
               np.linspace(int(nws_precip_colors_original[i][1:3], 16), int(nws_precip_colors_original[i + 1][1:3], 16),
                           500)]
        green = [val for val in np.linspace(int(nws_precip_colors_original[i][3:5], 16),
                                            int(nws_precip_colors_original[i + 1][3:5], 16), 500)]
        blue = [val for val in np.linspace(int(nws_precip_colors_original[i][5:7], 16),
                                           int(nws_precip_colors_original[i + 1][5:7], 16), 500)]
        # print("blue=",np.array(blue).shape)
        # stack2 = np.vstack([red, green, blue])
        # print("stack2=",stack2.shape)

        stack = np.vstack([red, green, blue]).T
        # print("stack=",stack.shape)
        color_int = stack if color_int == [] else np.concatenate((color_int, stack))
        # print("color_int=",color_int.shape)

        # i= 0  val= #04e9e7
        # blue= (500,)
        # stack2= (3, 500)
        # stack= (500, 3)
        # color_int= (500, 3)
        # ----
        # i= 12  val= #f800fd
        # blue= (500,)
        # stack2= (3, 500)
        # stack= (500, 3)
        # color_int= (6500, 3)
        # print('----')
    # print("=============")
    # print("color_int=",color_int.shape)
    color_code = []
    for val in color_int:
        color_code.append('#{:02X}{:02X}{:02X}'.format(int(val[0]), int(val[1]), int(val[2])))
    # print("color_code=",np.array(color_code).shape)
    color_code = np.concatenate([nan_zero, color_code])
    # print("color_code=",color_code.shape)

    return color_code