from bar_chart import bar_chart
from heap_map import heap_map
from line_chart import line_chart
if __name__ == '__main__':

    choice = int(input("输入您的需求：\n"
                       "生成热力图：1 \n"
                       "生成月走势图：2 \n"
                       "生成增长率图：3  \n"
                       "生成预测图：4 \n"
                       ""))
    if choice == 1:
        heap_map()
    elif choice == 2:
        line_chart(0)
    elif choice == 3:
        bar_chart()
    elif choice == 4:
        line_chart(1)
