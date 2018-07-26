# Baidu_XJTU_2018_company_logo_detection
百度-西交大·大数据竞赛2018复赛——商家招牌智能检测

1.代码运行环境
Python 3.5.3
Keras 2.1.3
Tensorflow 1.4.0-rc0

2.文件系统结构
.
│   ├── font 结果可视化时label的字体文件

│   ├── logs 模型打点，实施保存模型当前的权重

│   ├── model_data 放置预测用的模型以及辅助信息

│   ├── result 预测结果

│   ├── test.txt 待预测文件列表

│   ├── train.py 训练模型主程序

│   ├── train.txt 训练文件及label列表

│   ├── utils 预处理与结果可视化工具

│   ├── yolo.py 预测主程序

│   └── yolo3 模型文件

└   |── data  存放比赛用数据集（压缩文件中未包含，将官方下载的数据集放置即可）

       ├── test
       └── train

3.使用方法
预测
将训练好的模型文件yolo.h5放置于BaiduFusai/model_data文件夹中，运行BaiduFusai/yolo.py即可。
训练
我们提供了第一阶段训练好的模型trained_weights_stage_1.h5，可以将其放置于BaiduFusai/logs/000中进行训练。
如果要从头训练，将在coco上预训练的模型yolo_weights.h5放置于BaiduFusai/model_data文件夹中，将train.py第35行注释，并取消第34行注释，执行BaiduFuasi/train.py即可。
结果可视化
在预测之后，会给出生成BaiduFusai/result/YOLOv3.csv，使用utils/draw_result.py可以根据此文件绘制可视化结果。

4.算法说明
算法使用目标检测中著名的YOLOv3，模型主干来源于GitHub的开源项目(https://github.com/qqwweee/keras-yolo3)。
对于本赛题，我们首先做了一些数据预处理，使得输入数据满足模型定义的格式。该模型的label文件格式为
Image_file_path box1 box2 … boxN
其中
box格式为 x_min,y_min,x_max,y_max,class_id(无空格)
执行parse_train_txt.py文件可以将原始赛题数据集的train.txt文件转化成目标格式。

算法以验证集损失为依据，动态保存最优模型。所以将原始训练集划分为新的训练集和验证集。划分具体方式是将所有数据混洗，然后按照设定的切割比例（train.py main()函数中的val_split）划分。

模型的训练过程分为两个阶段。第一个阶段先冻结前面的层，Finetune最后几层。通过这一步就能得到一个不错的结果。我们提供了第一阶段训练结束的模型trained_weights_state_1.h5，可以直接用于第二阶段训练。第二阶段是解冻所有的层，以一个较低的学习率全局训练。第二步会消耗更多的显存，所以两个阶段选择了不同的batch size。

超参数的选择主要有iou, score阈值，图片尺寸等。调整前两项并不需要重新训练模型。

5.致谢
感谢队友给力的工作以及对我的指导！队友大佬的飞机票》》https://github.com/MoZhonglin
