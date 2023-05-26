#include <iostream>
#include <string.h>
#include <thread>
#include <mutex>
#include <unistd.h>
#include <time.h>
#include <opencv2/opencv.hpp>
#include <pthread.h>
#include <stdlib.h>
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"

using namespace cv;
using namespace std;
int brilho = 61;
int saturacao = 81;

vector<vector<Point>> detectar_triangulos_laranjas(Mat imagem, int brilho, int saturacao) {
    Mat hsv;
    cvtColor(imagem, hsv, COLOR_BGR2HSV);

    Scalar laranja_baixo(0, 80, 60);
    Scalar laranja_alto(10, saturacao, brilho);

    Mat mascara_laranja;
    inRange(hsv, laranja_baixo, laranja_alto, mascara_laranja);

    Mat kernel = getStructuringElement(MORPH_RECT, Size(5, 5));
    morphologyEx(mascara_laranja, mascara_laranja, MORPH_OPEN, kernel);

    vector<vector<Point>> contornos;
    findContours(mascara_laranja, contornos, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    vector<vector<Point>> triangulos_laranjas;

    for (const auto& contorno : contornos) {
        double perimetro = arcLength(contorno, true);
        vector<Point> aproximacao;
        approxPolyDP(contorno, aproximacao, 0.04 * perimetro, true);

        if (aproximacao.size() == 3) {
            triangulos_laranjas.push_back(aproximacao);
        }
    }

    return triangulos_laranjas;
}

void onTrackbarSaturacao(int valor, void* userdata) {
    saturacao = valor;
}

void onTrackbarBrilho(int valor, void* userdata) {
    brilho = valor;
}

int main() {
    namedWindow("Configuração", WINDOW_NORMAL);
    
    createTrackbar("Brilho   ", "Configuração", &brilho, 255, onTrackbarBrilho);
    createTrackbar("Saturação", "Configuração", &saturacao, 255, onTrackbarSaturacao);

    VideoCapture captura(0);

    if (!captura.isOpened()) {
        cout << "Não foi possível abrir a câmera." << endl;
        return -1;
    }

    while (true) {
        Mat frame;
        captura >> frame;

        if (frame.empty()) {
            break;
        }

        vector<vector<Point>> triangulos = detectar_triangulos_laranjas(frame, brilho, saturacao);

        for (const auto& triangulo : triangulos) {
            drawContours(frame, vector<vector<Point>>{triangulo}, 0, Scalar(0, 255, 0), 2);
        }

        imshow("Detecção de Triângulos Laranjas", frame);

        if (waitKey(1) == 'q') {
            break;
        }
    }

    captura.release();
    destroyAllWindows();

    return 0;
}