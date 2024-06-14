#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <time.h>
using namespace std;
using namespace cv;

Mat gray_hist; //直方图计算的结果
void CalHistogram(Mat& img);
void HistMap(Mat& img_src, Mat& img_obj);

int main()
{
    //注意imread后不加参数，默认读取进来的是RGB图像
    Mat img_src = imread("/home/tsdl/SBMV/数据/VG2S/BC23#1_#3_2024021908510808.png", IMREAD_COLOR);
    Mat img_obj = imread("/home/tsdl/SBMV/数据/VG2S/VG2S_train/VG2S_down/vg2s#1_2419299073#3_2024051610593010.png", IMREAD_COLOR);
    Mat imgOutput; //规定化后的输出图像

    clock_t begin = clock();
    //分割原图像通道
    vector<Mat> src_channels;
    Mat src_blue, src_green, src_red;
    split(img_src, src_channels);
    src_blue = src_channels.at(0);
    src_green = src_channels.at(1);
    src_red = src_channels.at(2);
    //分割目标图像通道
    vector<Mat> obj_channels;
    Mat obj_blue, obj_green, obj_red;
    split(img_obj, obj_channels);
    obj_blue = obj_channels.at(0);
    obj_green = obj_channels.at(1);
    obj_red = obj_channels.at(2);

    //分别对BGR通道做直方图规定化
    HistMap(src_blue, obj_blue);
    HistMap(src_green, obj_green);
    HistMap(src_red, obj_red);
    //合并通道，输出结果
    merge(src_channels, imgOutput);
    clock_t end = clock();
    double duration = double(end - begin)/CLOCKS_PER_SEC;
    cout << "Time Cost: " << duration << endl;

    //显示图像
    imshow("img_src", img_src);
    imshow("img_obj", img_obj);
    imshow("imgOutput", imgOutput);
    waitKey(0);

    return 0;
}

void CalHistogram(Mat& img)
{
    if (img.empty())
        return;

    //设定bin数目
    int histsize = 256;

    //设定取值范围
    float range[] = { 0, 256 };
    const float* histRange = { range };

    //调用OpenCV函数计算直方图，计算结果保存到gray_hist中
    calcHist(&img, 1, 0, Mat(), gray_hist, 1, &histsize, &histRange);
}

void HistMap(Mat& img_src, Mat& img_obj)
{
    int i, j; //循环变量
    double gray_temp = 0; //中间结果，用于计算累计直方图
    double totalPixel; //像素总数

    //计算原图像直方图，并归一化到(0, 1)
    CalHistogram(img_src);
    totalPixel = img_src.rows * img_src.cols;
    double srcHist[256];
    for (i = 0; i < 256; i++)
    {
        srcHist[i] = gray_hist.at<float>(i) / totalPixel;
    }

    //计算原图像直方图的累计概率 0 ~ 1
    double srcCumHist[256];
    for (i = 0; i < 256; i++)
    {
        gray_temp = 0;
        for (j = 0; j <= i; j++)
        {
            gray_temp += srcHist[j];
        }
        srcCumHist[i] = gray_temp;
    }

    //计算目标图像直方图
    CalHistogram(img_obj);
    totalPixel = img_obj.rows * img_obj.cols;
    double objHist[256];
    for (i = 0; i < 256; i++)
    {
        objHist[i] = gray_hist.at<float>(i) / totalPixel;
    }

    //计算目标图像直方图的累计概率 0 ~ 1
    double objCumHist[256];
    for (i = 0; i < 256; i++)
    {
        gray_temp = 0;
        for (j = 0; j <= i; j++)
        {
            gray_temp += objHist[j];
        }
        objCumHist[i] = gray_temp;
    }

    //GML组映射
    double min = 1; //设置成一个≥1的数即可
    uchar map[256]; //输入->输出的映射关系
    uchar groop[256]; //分组序号
    for (i = 0; i < 256; i++)
    {
        groop[i] = -1; //初始化
    }
    for (i = 0; i < 256; i++) //遍历目标图像的累计直方图
    {
        if (objHist[i] == 0) //如果该位置的直方图为0，可以跳出这次循环了，因为不会有点映射到这里来
        {
            if (i > 0)
                groop[i] = groop[i - 1];
            continue;
        }
        min = 1;
        for (j = 0; j < 256; j++)  //遍历原图像，寻找两个直方图距离最接近的点
        {
            if (abs(objCumHist[i] - srcCumHist[j]) < min)
            {
                min = abs(objCumHist[i] - srcCumHist[j]);
                groop[i] = j; //最接近的直方图位置（原图像），记录分组序号
            }
        }
        if (i == 0) //灰度值为0的情况有点特殊
        {
            for (int pos = 0; pos <= groop[i]; pos++)
                map[pos] = 0;
        }
        else
        {
            for (int pos = groop[i - 1] + 1; pos <= groop[i]; pos++) //属于同一组内的元素，映射到同一个灰度值
                map[pos] = i; //建立映射关系
        }
    }

    //根据映射关系进行点运算，修改原图像
    uchar* p = NULL; //用于遍历像素的指针
    int width = img_src.cols;
    int height = img_src.rows;
    for (i = 0; i < height; i++)
    {
        p = img_src.ptr<uchar>(i); //获取第i行的首地址
        for (j = 0; j < width; j++)
        {
            p[j] = map[p[j]];
        }
    }
}