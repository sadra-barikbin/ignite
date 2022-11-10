import sys
from unittest.mock import patch

import numpy as np
import pytest
import torch
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from ignite.metrics import MeanAveragePrecision

torch.set_printoptions(linewidth=200)
np.set_printoptions(linewidth=200)


@pytest.fixture
def coco_val2017_sample():
    gt = [
        torch.tensor(
            [
                [86.29, 342.29, 280.45, 507.69, 59.00],
                [100.64, 33.17, 445.01, 630.72, 1.00],
                [396.78, 503.17, 480.00, 639.83, 1.00],
            ]
        ),
        torch.tensor([[73.15, 17.21, 525.83, 420.84, 18.00], [441.32, 248.01, 598.31, 385.86, 34.00]]),
        torch.tensor(
            [
                [238.74, 419.10, 345.17, 572.40, 1.00],
                [346.88, 150.45, 372.49, 222.67, 1.00],
                [156.20, 184.21, 182.26, 244.70, 1.00],
                [120.97, 181.28, 143.40, 253.87, 1.00],
                [98.72, 186.11, 123.08, 255.08, 1.00],
                [63.49, 189.41, 83.63, 237.39, 1.00],
                [51.88, 165.18, 72.86, 193.85, 1.00],
                [212.53, 148.52, 235.60, 169.72, 1.00],
                [24.71, 183.87, 53.33, 239.24, 1.00],
                [219.79, 450.58, 259.89, 568.97, 35.00],
            ]
        ),
        torch.tensor([[187.69, 83.33, 524.22, 244.04, 5.00]]),
        torch.tensor(
            [
                [366.81, 311.35, 452.21, 377.36, 4.00],
                [207.79, 272.69, 268.19, 286.07, 9.00],
                [225.85, 280.49, 286.97, 299.48, 9.00],
                [372.29, 267.53, 378.99, 284.08, 1.00],
                [380.49, 265.75, 384.55, 280.14, 1.00],
                [383.77, 265.81, 389.22, 282.09, 1.00],
                [462.07, 267.86, 465.44, 278.96, 1.00],
                [150.33, 288.74, 277.12, 363.00, 8.00],
                [377.82, 267.73, 381.55, 282.47, 1.00],
                [427.84, 272.41, 434.51, 279.67, 1.00],
                [280.83, 276.41, 327.02, 291.01, 9.00],
                [332.52, 208.75, 373.61, 282.90, 9.00],
                [571.89, 265.22, 587.20, 270.15, 9.00],
                [297.68, 263.47, 350.83, 287.53, 9.00],
                [115.99, 335.23, 220.54, 386.99, 15.00],
                [467.58, 266.66, 480.25, 273.15, 28.00],
                [310.60, 183.89, 326.46, 189.21, 38.00],
                [307.86, 166.61, 311.99, 171.10, 38.00],
                [294.98, 144.03, 297.05, 146.34, 38.00],
                [357.78, 228.79, 366.04, 234.15, 38.00],
                [333.89, 202.44, 338.67, 206.65, 38.00],
                [385.79, 253.31, 392.87, 256.32, 38.00],
                [346.17, 214.34, 349.64, 217.03, 38.00],
                [458.59, 268.43, 461.56, 278.74, 1.00],
                [500.29, 273.39, 505.81, 278.91, 1.00],
                [493.66, 273.21, 498.91, 279.88, 1.00],
                [419.23, 267.92, 424.14, 279.16, 1.00],
                [472.35, 270.79, 475.99, 274.69, 1.00],
                [164.62, 163.86, 199.66, 293.74, 9.00],
                [390.74, 271.16, 394.72, 278.07, 1.00],
                [414.18, 267.71, 419.65, 279.12, 1.00],
                [601.50, 264.23, 636.20, 274.04, 9.00],
                [618.35, 265.79, 620.91, 267.66, 28.00],
                [604.53, 274.15, 625.66, 288.61, 62.00],
                [462.00, 267.00, 592.00, 296.00, 1.00],
            ]
        ),
        torch.tensor([[360.00, 101.08, 629.19, 317.30, 73.00], [393.66, 232.18, 568.67, 275.55, 76.00]]),
        torch.tensor(
            [
                [160.42, 362.24, 166.04, 371.03, 32.00],
                [256.82, 342.07, 276.85, 386.79, 1.00],
                [148.56, 349.60, 176.82, 404.29, 1.00],
                [275.99, 343.59, 302.30, 393.31, 1.00],
                [514.65, 356.77, 533.58, 382.69, 1.00],
                [128.24, 353.34, 152.80, 379.24, 1.00],
                [501.92, 365.74, 518.64, 398.10, 1.00],
                [118.03, 394.53, 183.94, 472.52, 22.00],
                [248.65, 389.73, 302.70, 457.84, 22.00],
                [294.82, 400.78, 400.91, 449.74, 22.00],
                [497.69, 391.02, 536.86, 435.73, 22.00],
                [604.12, 383.83, 640.00, 430.23, 22.00],
                [384.24, 389.75, 424.11, 444.46, 22.00],
                [140.66, 363.06, 142.43, 369.08, 32.00],
                [262.97, 369.03, 279.47, 392.67, 1.00],
                [375.06, 365.29, 393.36, 404.30, 1.00],
                [398.69, 354.63, 419.99, 383.35, 1.00],
                [620.99, 357.90, 637.65, 389.63, 1.00],
                [355.48, 363.69, 377.04, 400.51, 1.00],
                [340.07, 371.29, 359.26, 406.30, 1.00],
                [387.53, 351.02, 401.71, 385.15, 1.00],
            ]
        ),
        torch.tensor([[325.08, 243.21, 429.04, 339.98, 16.00], [478.82, 193.74, 598.75, 286.00, 16.00]]),
        torch.tensor(
            [
                [382.34, 157.07, 414.30, 182.86, 39.00],
                [232.06, 249.10, 327.87, 368.84, 1.00],
                [318.09, 172.94, 388.67, 271.20, 1.00],
                [362.64, 211.51, 409.17, 264.63, 1.00],
                [389.87, 183.89, 442.03, 262.58, 1.00],
                [175.72, 106.28, 211.25, 180.00, 1.00],
                [135.33, 134.34, 161.36, 170.05, 1.00],
                [94.48, 154.32, 120.27, 186.96, 1.00],
                [47.17, 171.37, 68.74, 205.06, 1.00],
                [455.26, 92.87, 490.92, 121.53, 1.00],
                [463.65, 112.88, 497.27, 143.09, 1.00],
                [291.70, 186.36, 313.02, 206.34, 1.00],
                [424.16, 197.69, 435.12, 208.28, 62.00],
                [57.83, 132.90, 86.78, 160.73, 1.00],
                [364.89, 239.80, 376.76, 252.37, 40.00],
                [427.17, 177.22, 452.42, 193.30, 62.00],
                [479.15, 175.84, 503.98, 204.07, 62.00],
                [117.82, 152.30, 150.24, 209.05, 1.00],
                [466.04, 177.11, 492.57, 193.21, 62.00],
                [451.33, 197.51, 478.60, 209.86, 62.00],
                [399.53, 177.11, 427.04, 193.40, 62.00],
                [621.99, 172.38, 640.00, 185.09, 62.00],
                [586.14, 175.25, 597.78, 202.80, 62.00],
                [0.00, 0.00, 639.00, 218.00, 1.00],
            ]
        ),
        torch.tensor(
            [
                [272.10, 200.23, 424.07, 480.00, 18.00],
                [181.23, 86.28, 208.67, 159.81, 44.00],
                [174.74, 0.00, 435.78, 220.79, 70.00],
            ]
        ),
    ]

    pred = [
        torch.tensor(
            [
                [104.00, 46.00, 440.00, 635.00, 1.00, 1.00],
                [82.00, 348.00, 283.00, 501.00, 1.00, 59.00],
                [393.00, 482.00, 479.00, 639.00, 0.96, 1.00],
                [0.00, 455.00, 190.00, 559.00, 0.68, 84.00],
                [141.00, 0.00, 202.00, 79.00, 0.36, 84.00],
                [79.00, 31.00, 116.00, 100.00, 0.35, 1.00],
                [149.00, 26.00, 196.00, 70.00, 0.31, 1.00],
                [0.00, 478.00, 202.00, 610.00, 0.26, 84.00],
                [267.00, 269.00, 454.00, 636.00, 0.25, 1.00],
                [29.00, 340.00, 301.00, 601.00, 0.17, 67.00],
                [260.00, 384.00, 299.00, 515.00, 0.14, 49.00],
                [123.00, 326.00, 307.00, 366.00, 0.11, 49.00],
                [430.00, 478.00, 480.00, 563.00, 0.08, 1.00],
                [1.00, 589.00, 92.00, 637.00, 0.06, 62.00],
                [5.00, 533.00, 180.00, 608.00, 0.06, 84.00],
                [0.00, 588.00, 93.00, 637.00, 0.06, 1.00],
                [41.00, 474.00, 193.00, 513.00, 0.05, 49.00],
            ]
        ),
        torch.tensor(
            [
                [64.00, 8.00, 536.00, 421.00, 1.00, 18.00],
                [443.00, 249.00, 604.00, 384.00, 1.00, 34.00],
                [108.00, 273.00, 303.00, 378.00, 0.12, 18.00],
                [227.00, 168.00, 512.00, 426.00, 0.07, 18.00],
            ]
        ),
        torch.tensor(
            [
                [347.00, 150.00, 371.00, 223.00, 1.00, 1.00],
                [242.00, 418.00, 342.00, 566.00, 1.00, 1.00],
                [155.00, 183.00, 182.00, 245.00, 0.99, 1.00],
                [24.00, 183.00, 54.00, 239.00, 0.99, 1.00],
                [0.00, 186.00, 13.00, 242.00, 0.97, 1.00],
                [61.00, 183.00, 85.00, 239.00, 0.97, 1.00],
                [122.00, 182.00, 145.00, 257.00, 0.94, 1.00],
                [95.00, 182.00, 123.00, 263.00, 0.92, 1.00],
                [220.00, 452.00, 329.00, 571.00, 0.91, 35.00],
                [318.00, 628.00, 350.00, 639.00, 0.82, 1.00],
                [51.00, 161.00, 73.00, 193.00, 0.80, 1.00],
                [220.00, 451.00, 263.00, 566.00, 0.78, 35.00],
                [95.00, 162.00, 124.00, 197.00, 0.75, 1.00],
                [81.00, 612.00, 110.00, 640.00, 0.68, 1.00],
                [211.00, 148.00, 235.00, 170.00, 0.63, 1.00],
                [8.00, 237.00, 97.00, 279.00, 0.32, 15.00],
                [0.00, 544.00, 423.00, 637.00, 0.26, 7.00],
                [233.00, 629.00, 262.00, 640.00, 0.24, 1.00],
                [0.00, 237.00, 14.00, 259.00, 0.24, 62.00],
                [0.00, 544.00, 418.00, 636.00, 0.23, 9.00],
                [173.00, 207.00, 183.00, 228.00, 0.23, 31.00],
                [121.00, 149.00, 149.00, 195.00, 0.18, 35.00],
                [14.00, 239.00, 36.00, 261.00, 0.18, 62.00],
                [30.00, 238.00, 49.00, 261.00, 0.15, 62.00],
                [112.00, 194.00, 121.00, 208.00, 0.13, 27.00],
                [32.00, 239.00, 58.00, 270.00, 0.11, 62.00],
                [99.00, 193.00, 117.00, 215.00, 0.09, 27.00],
                [140.00, 621.00, 160.00, 640.00, 0.08, 1.00],
                [0.00, 197.00, 2.00, 271.00, 0.08, 1.00],
                [0.00, 118.00, 4.00, 143.00, 0.07, 1.00],
                [169.00, 199.00, 181.00, 241.00, 0.06, 1.00],
                [182.00, 210.00, 200.00, 228.00, 0.06, 27.00],
                [0.00, 237.00, 13.00, 253.00, 0.05, 31.00],
            ]
        ),
        torch.tensor([[192.00, 80.00, 516.00, 240.00, 1.00, 5.00]]),
        torch.tensor(
            [
                [365.00, 311.00, 453.00, 378.00, 1.00, 4.00],
                [113.00, 334.00, 220.00, 385.00, 1.00, 15.00],
                [224.00, 281.00, 289.00, 299.00, 0.96, 9.00],
                [290.00, 272.00, 342.00, 288.00, 0.93, 9.00],
                [310.00, 183.00, 326.00, 189.00, 0.93, 38.00],
                [151.00, 284.00, 276.00, 366.00, 0.92, 8.00],
                [371.00, 267.00, 377.00, 283.00, 0.92, 1.00],
                [384.00, 265.00, 389.00, 280.00, 0.91, 1.00],
                [332.00, 267.00, 374.00, 282.00, 0.89, 9.00],
                [307.00, 166.00, 312.00, 170.00, 0.85, 38.00],
                [377.00, 269.00, 382.00, 283.00, 0.83, 1.00],
                [195.00, 269.00, 269.00, 286.00, 0.74, 9.00],
                [418.00, 268.00, 424.00, 279.00, 0.73, 1.00],
                [413.00, 267.00, 418.00, 279.00, 0.72, 1.00],
                [427.00, 272.00, 434.00, 279.00, 0.71, 1.00],
                [282.00, 275.00, 326.00, 290.00, 0.71, 9.00],
                [166.00, 267.00, 291.00, 289.00, 0.69, 9.00],
                [585.00, 273.00, 590.00, 285.00, 0.68, 1.00],
                [458.00, 268.00, 462.00, 279.00, 0.68, 1.00],
                [294.00, 143.00, 297.00, 147.00, 0.65, 38.00],
                [496.00, 271.00, 500.00, 279.00, 0.65, 1.00],
                [333.00, 201.00, 339.00, 207.00, 0.63, 38.00],
                [578.00, 273.00, 583.00, 282.00, 0.61, 1.00],
                [501.00, 271.00, 506.00, 280.00, 0.61, 1.00],
                [163.00, 270.00, 212.00, 291.00, 0.61, 9.00],
                [390.00, 270.00, 393.00, 278.00, 0.61, 1.00],
                [571.00, 265.00, 587.00, 270.00, 0.61, 9.00],
                [380.00, 265.00, 385.00, 282.00, 0.59, 1.00],
                [153.00, 287.00, 276.00, 366.00, 0.48, 9.00],
                [514.00, 272.00, 527.00, 280.00, 0.47, 1.00],
                [471.00, 270.00, 476.00, 280.00, 0.47, 1.00],
                [474.00, 266.00, 478.00, 274.00, 0.42, 1.00],
                [547.00, 273.00, 558.00, 280.00, 0.39, 1.00],
                [331.00, 211.00, 374.00, 282.00, 0.35, 9.00],
                [474.00, 266.00, 479.00, 280.00, 0.34, 1.00],
                [494.00, 272.00, 498.00, 279.00, 0.32, 1.00],
                [251.00, 264.00, 257.00, 269.00, 0.32, 1.00],
                [281.00, 275.00, 326.00, 295.00, 0.30, 28.00],
                [384.00, 252.00, 393.00, 255.00, 0.29, 9.00],
                [322.00, 272.00, 350.00, 287.00, 0.27, 9.00],
                [163.00, 204.00, 215.00, 289.00, 0.26, 9.00],
                [299.00, 212.00, 344.00, 288.00, 0.23, 9.00],
                [459.00, 268.00, 464.00, 279.00, 0.23, 1.00],
                [601.00, 267.00, 635.00, 273.00, 0.23, 9.00],
                [164.00, 262.00, 206.00, 286.00, 0.23, 9.00],
                [576.00, 273.00, 580.00, 281.00, 0.21, 1.00],
                [571.00, 273.00, 575.00, 280.00, 0.19, 1.00],
                [216.00, 268.00, 284.00, 283.00, 0.18, 9.00],
                [219.00, 272.00, 286.00, 292.00, 0.17, 9.00],
                [571.00, 266.00, 587.00, 270.00, 0.16, 28.00],
                [493.00, 272.00, 497.00, 279.00, 0.14, 1.00],
                [600.00, 266.00, 636.00, 279.00, 0.14, 9.00],
                [150.00, 288.00, 276.00, 367.00, 0.14, 3.00],
                [172.00, 171.00, 254.00, 287.00, 0.14, 9.00],
                [469.00, 266.00, 479.00, 281.00, 0.13, 1.00],
                [465.00, 270.00, 472.00, 280.00, 0.13, 1.00],
                [283.00, 273.00, 327.00, 290.00, 0.13, 42.00],
                [250.00, 210.00, 283.00, 280.00, 0.12, 9.00],
                [497.00, 271.00, 504.00, 280.00, 0.12, 1.00],
                [514.00, 271.00, 527.00, 280.00, 0.11, 62.00],
                [465.00, 271.00, 473.00, 280.00, 0.10, 62.00],
                [626.00, 269.00, 640.00, 283.00, 0.10, 3.00],
                [462.00, 268.00, 466.00, 279.00, 0.09, 1.00],
                [301.00, 270.00, 326.00, 290.00, 0.09, 9.00],
                [573.00, 274.00, 576.00, 281.00, 0.09, 1.00],
                [384.00, 252.00, 393.00, 255.00, 0.08, 38.00],
                [575.00, 275.00, 579.00, 281.00, 0.07, 1.00],
                [602.00, 266.00, 635.00, 272.00, 0.07, 28.00],
                [225.00, 280.00, 285.00, 299.00, 0.07, 42.00],
                [118.00, 311.00, 253.00, 377.00, 0.07, 8.00],
                [633.00, 271.00, 640.00, 283.00, 0.07, 3.00],
                [547.00, 273.00, 552.00, 280.00, 0.06, 1.00],
                [464.00, 267.00, 477.00, 281.00, 0.06, 62.00],
                [467.00, 266.00, 477.00, 272.00, 0.06, 28.00],
                [242.00, 281.00, 321.00, 300.00, 0.06, 9.00],
                [164.00, 215.00, 185.00, 276.00, 0.06, 9.00],
                [164.00, 256.00, 185.00, 274.00, 0.05, 9.00],
            ]
        ),
        torch.tensor(
            [
                [359.00, 101.00, 626.00, 315.00, 1.00, 73.00],
                [0.00, 8.00, 176.00, 261.00, 0.92, 67.00],
                [386.00, 230.00, 565.00, 275.00, 0.79, 76.00],
                [123.00, 74.00, 635.00, 470.00, 0.30, 8.00],
                [373.00, 227.00, 598.00, 300.00, 0.29, 76.00],
                [122.00, 90.00, 610.00, 476.00, 0.27, 33.00],
                [0.00, 8.00, 149.00, 159.00, 0.26, 67.00],
                [359.00, 102.00, 553.00, 241.00, 0.24, 72.00],
                [588.00, 240.00, 639.00, 350.00, 0.23, 15.00],
                [264.00, 64.00, 339.00, 115.00, 0.21, 27.00],
                [0.00, 36.00, 41.00, 52.00, 0.15, 75.00],
                [305.00, 0.00, 365.00, 70.00, 0.14, 62.00],
                [39.00, 42.00, 77.00, 52.00, 0.14, 77.00],
                [0.00, 38.00, 39.00, 53.00, 0.12, 77.00],
                [567.00, 8.00, 638.00, 242.00, 0.12, 62.00],
                [0.00, 18.00, 40.00, 46.00, 0.12, 84.00],
                [130.00, 116.00, 630.00, 470.00, 0.11, 67.00],
                [596.00, 239.00, 639.00, 276.00, 0.08, 67.00],
                [119.00, 100.00, 558.00, 475.00, 0.08, 3.00],
                [117.00, 69.00, 551.00, 469.00, 0.07, 4.00],
                [595.00, 14.00, 639.00, 322.00, 0.07, 62.00],
                [264.00, 64.00, 339.00, 114.00, 0.06, 31.00],
                [28.00, 48.00, 90.00, 69.00, 0.06, 84.00],
                [62.00, 0.00, 94.00, 28.00, 0.06, 62.00],
                [2.00, 176.00, 136.00, 329.00, 0.06, 84.00],
                [1.00, 0.00, 88.00, 23.00, 0.06, 62.00],
                [0.00, 34.00, 42.00, 52.00, 0.05, 84.00],
                [0.00, 19.00, 24.00, 41.00, 0.05, 84.00],
                [589.00, 232.00, 639.00, 352.00, 0.05, 62.00],
                [39.00, 41.00, 76.00, 50.00, 0.05, 48.00],
            ]
        ),
        torch.tensor(
            [
                [247.00, 389.00, 298.00, 455.00, 1.00, 22.00],
                [115.00, 396.00, 185.00, 471.00, 1.00, 22.00],
                [294.00, 395.00, 400.00, 450.00, 1.00, 22.00],
                [499.00, 384.00, 538.00, 436.00, 1.00, 22.00],
                [604.00, 385.00, 640.00, 430.00, 1.00, 22.00],
                [147.00, 348.00, 176.00, 401.00, 1.00, 1.00],
                [127.00, 352.00, 150.00, 396.00, 1.00, 1.00],
                [274.00, 343.00, 301.00, 393.00, 1.00, 1.00],
                [255.00, 342.00, 277.00, 388.00, 0.99, 1.00],
                [622.00, 358.00, 636.00, 390.00, 0.99, 1.00],
                [498.00, 354.00, 512.00, 388.00, 0.99, 1.00],
                [378.00, 389.00, 423.00, 444.00, 0.99, 22.00],
                [357.00, 364.00, 377.00, 401.00, 0.98, 1.00],
                [610.00, 367.00, 624.00, 389.00, 0.98, 1.00],
                [516.00, 356.00, 531.00, 383.00, 0.98, 1.00],
                [263.00, 369.00, 279.00, 394.00, 0.97, 1.00],
                [370.00, 363.00, 395.00, 405.00, 0.96, 1.00],
                [612.00, 358.00, 622.00, 374.00, 0.96, 1.00],
                [339.00, 372.00, 356.00, 400.00, 0.96, 1.00],
                [503.00, 366.00, 517.00, 389.00, 0.95, 1.00],
                [384.00, 349.00, 401.00, 376.00, 0.94, 1.00],
                [397.00, 352.00, 419.00, 390.00, 0.93, 1.00],
                [388.00, 364.00, 405.00, 392.00, 0.69, 1.00],
                [378.00, 362.00, 396.00, 392.00, 0.59, 1.00],
                [402.00, 352.00, 419.00, 374.00, 0.55, 1.00],
                [615.00, 363.00, 630.00, 390.00, 0.48, 1.00],
                [394.00, 353.00, 410.00, 384.00, 0.41, 1.00],
                [512.00, 358.00, 531.00, 396.00, 0.30, 1.00],
                [407.00, 369.00, 420.00, 392.00, 0.28, 15.00],
                [519.00, 366.00, 533.00, 386.00, 0.20, 15.00],
                [407.00, 355.00, 421.00, 389.00, 0.17, 1.00],
                [257.00, 356.00, 282.00, 393.00, 0.16, 1.00],
                [607.00, 372.00, 614.00, 387.00, 0.15, 1.00],
                [262.00, 346.00, 279.00, 379.00, 0.14, 1.00],
                [116.00, 352.00, 154.00, 412.00, 0.13, 1.00],
                [338.00, 371.00, 369.00, 403.00, 0.13, 1.00],
                [381.00, 356.00, 399.00, 383.00, 0.12, 1.00],
                [125.00, 370.00, 176.00, 399.00, 0.12, 15.00],
                [380.00, 361.00, 406.00, 399.00, 0.11, 1.00],
                [256.00, 342.00, 299.00, 396.00, 0.10, 1.00],
                [149.00, 373.00, 176.00, 401.00, 0.10, 15.00],
                [407.00, 368.00, 420.00, 392.00, 0.08, 62.00],
                [380.00, 366.00, 421.00, 394.00, 0.08, 15.00],
                [11.00, 10.00, 464.00, 191.00, 0.07, 7.00],
                [353.00, 373.00, 414.00, 402.00, 0.07, 15.00],
                [250.00, 367.00, 279.00, 408.00, 0.07, 1.00],
                [126.00, 375.00, 155.00, 398.00, 0.06, 15.00],
                [501.00, 366.00, 521.00, 402.00, 0.06, 1.00],
                [349.00, 394.00, 403.00, 448.00, 0.06, 22.00],
                [352.00, 362.00, 395.00, 411.00, 0.05, 1.00],
            ]
        ),
        torch.tensor(
            [
                [476.00, 188.00, 596.00, 290.00, 1.00, 16.00],
                [323.00, 250.00, 426.00, 336.00, 1.00, 16.00],
                [381.00, 255.00, 427.00, 313.00, 0.20, 16.00],
                [23.00, 60.00, 634.00, 377.00, 0.09, 67.00],
            ]
        ),
        torch.tensor(
            [
                [232.00, 248.00, 325.00, 368.00, 1.00, 1.00],
                [318.00, 174.00, 387.00, 269.00, 1.00, 1.00],
                [362.00, 214.00, 408.00, 265.00, 0.99, 1.00],
                [391.00, 187.00, 443.00, 264.00, 0.99, 1.00],
                [375.00, 156.00, 413.00, 187.00, 0.97, 39.00],
                [529.00, 185.00, 560.00, 208.00, 0.85, 1.00],
                [315.00, 181.00, 341.00, 205.00, 0.83, 1.00],
                [165.00, 181.00, 201.00, 209.00, 0.79, 1.00],
                [90.00, 154.00, 120.00, 187.00, 0.76, 1.00],
                [45.00, 172.00, 70.00, 208.00, 0.74, 1.00],
                [369.00, 212.00, 385.00, 229.00, 0.74, 40.00],
                [174.00, 105.00, 211.00, 178.00, 0.74, 1.00],
                [288.00, 152.00, 317.00, 183.00, 0.72, 1.00],
                [42.00, 150.00, 77.00, 185.00, 0.72, 1.00],
                [599.00, 146.00, 635.00, 207.00, 0.69, 1.00],
                [492.00, 179.00, 525.00, 209.00, 0.69, 1.00],
                [467.00, 142.00, 496.00, 177.00, 0.69, 1.00],
                [16.00, 168.00, 49.00, 210.00, 0.67, 1.00],
                [458.00, 94.00, 490.00, 122.00, 0.66, 1.00],
                [584.00, 122.00, 617.00, 157.00, 0.64, 1.00],
                [500.00, 141.00, 532.00, 178.00, 0.64, 1.00],
                [97.00, 186.00, 123.00, 209.00, 0.63, 1.00],
                [438.00, 143.00, 467.00, 193.00, 0.63, 1.00],
                [0.00, 175.00, 2.00, 215.00, 0.62, 1.00],
                [384.00, 110.00, 412.00, 146.00, 0.62, 1.00],
                [525.00, 156.00, 554.00, 191.00, 0.62, 1.00],
                [117.00, 153.00, 148.00, 189.00, 0.62, 1.00],
                [292.00, 186.00, 314.00, 205.00, 0.60, 1.00],
                [464.00, 176.00, 492.00, 192.00, 0.59, 62.00],
                [304.00, 309.00, 313.00, 319.00, 0.58, 40.00],
                [263.00, 180.00, 291.00, 206.00, 0.56, 1.00],
                [210.00, 60.00, 247.00, 148.00, 0.54, 1.00],
                [287.00, 72.00, 316.00, 108.00, 0.53, 1.00],
                [519.00, 98.00, 544.00, 138.00, 0.53, 1.00],
                [550.00, 157.00, 583.00, 206.00, 0.50, 1.00],
                [180.00, 31.00, 211.00, 65.00, 0.50, 1.00],
                [404.00, 143.00, 432.00, 185.00, 0.49, 1.00],
                [137.00, 85.00, 160.00, 110.00, 0.49, 1.00],
                [363.00, 232.00, 369.00, 241.00, 0.45, 40.00],
                [352.00, 149.00, 385.00, 179.00, 0.44, 1.00],
                [531.00, 110.00, 561.00, 152.00, 0.43, 1.00],
                [362.00, 231.00, 377.00, 243.00, 0.43, 40.00],
                [490.00, 84.00, 517.00, 126.00, 0.43, 1.00],
                [315.00, 121.00, 339.00, 156.00, 0.43, 1.00],
                [623.00, 73.00, 640.00, 91.00, 0.43, 28.00],
                [223.00, 88.00, 252.00, 116.00, 0.42, 31.00],
                [462.00, 176.00, 491.00, 208.00, 0.40, 62.00],
                [587.00, 13.00, 610.00, 49.00, 0.40, 1.00],
                [310.00, 104.00, 334.00, 129.00, 0.39, 1.00],
                [425.00, 176.00, 454.00, 193.00, 0.39, 62.00],
                [134.00, 132.00, 163.00, 174.00, 0.39, 1.00],
                [183.00, 167.00, 205.00, 206.00, 0.39, 1.00],
                [320.00, 200.00, 328.00, 208.00, 0.38, 37.00],
                [50.00, 120.00, 73.00, 148.00, 0.38, 1.00],
                [286.00, 47.00, 318.00, 87.00, 0.38, 1.00],
                [486.00, 129.00, 508.00, 158.00, 0.37, 1.00],
                [259.00, 149.00, 288.00, 185.00, 0.36, 1.00],
                [87.00, 75.00, 114.00, 125.00, 0.34, 1.00],
                [160.00, 50.00, 183.00, 77.00, 0.34, 1.00],
                [423.00, 176.00, 453.00, 208.00, 0.33, 62.00],
                [36.00, 106.00, 58.00, 132.00, 0.32, 1.00],
                [0.00, 191.00, 1.00, 214.00, 0.31, 1.00],
                [603.00, 97.00, 623.00, 125.00, 0.30, 1.00],
                [499.00, 114.00, 524.00, 143.00, 0.30, 1.00],
                [392.00, 211.00, 403.00, 226.00, 0.30, 40.00],
                [526.00, 104.00, 555.00, 142.00, 0.28, 1.00],
                [362.00, 62.00, 392.00, 99.00, 0.28, 1.00],
                [9.00, 148.00, 37.00, 198.00, 0.28, 1.00],
                [331.00, 86.00, 361.00, 121.00, 0.27, 1.00],
                [223.00, 90.00, 252.00, 117.00, 0.27, 27.00],
                [451.00, 195.00, 479.00, 208.00, 0.27, 62.00],
                [583.00, 100.00, 614.00, 134.00, 0.26, 1.00],
                [459.00, 107.00, 494.00, 143.00, 0.25, 1.00],
                [288.00, 124.00, 317.00, 164.00, 0.25, 1.00],
                [189.00, 117.00, 210.00, 140.00, 0.25, 27.00],
                [73.00, 156.00, 95.00, 189.00, 0.25, 1.00],
                [286.00, 4.00, 319.00, 40.00, 0.24, 1.00],
                [17.00, 150.00, 37.00, 173.00, 0.24, 1.00],
                [314.00, 68.00, 340.00, 107.00, 0.24, 1.00],
                [582.00, 122.00, 618.00, 192.00, 0.23, 1.00],
                [474.00, 25.00, 503.00, 95.00, 0.23, 1.00],
                [154.00, 170.00, 176.00, 197.00, 0.23, 1.00],
                [473.00, 153.00, 489.00, 175.00, 0.23, 1.00],
                [154.00, 126.00, 181.00, 173.00, 0.23, 1.00],
                [58.00, 83.00, 92.00, 121.00, 0.23, 1.00],
                [92.00, 28.00, 120.00, 60.00, 0.23, 1.00],
                [368.00, 234.00, 380.00, 243.00, 0.22, 40.00],
                [565.00, 15.00, 584.00, 42.00, 0.21, 1.00],
                [56.00, 131.00, 86.00, 161.00, 0.21, 1.00],
                [431.00, 131.00, 446.00, 161.00, 0.21, 1.00],
                [69.00, 186.00, 91.00, 208.00, 0.21, 1.00],
                [261.00, 29.00, 290.00, 69.00, 0.20, 1.00],
                [110.00, 82.00, 141.00, 130.00, 0.20, 1.00],
                [365.00, 240.00, 374.00, 247.00, 0.19, 40.00],
                [150.00, 106.00, 184.00, 140.00, 0.19, 1.00],
                [554.00, 106.00, 575.00, 154.00, 0.18, 1.00],
                [12.00, 140.00, 39.00, 172.00, 0.17, 1.00],
                [109.00, 141.00, 127.00, 164.00, 0.17, 1.00],
                [452.00, 182.00, 485.00, 208.00, 0.17, 62.00],
                [617.00, 104.00, 637.00, 129.00, 0.17, 1.00],
            ]
        ),
        torch.tensor(
            [
                [268.00, 199.00, 423.00, 476.00, 1.00, 18.00],
                [175.00, 2.00, 368.00, 215.00, 0.99, 70.00],
                [179.00, 67.00, 212.00, 160.00, 0.95, 44.00],
                [118.00, 4.00, 392.00, 305.00, 0.66, 70.00],
                [113.00, 2.00, 261.00, 352.00, 0.60, 70.00],
                [129.00, 168.00, 249.00, 349.00, 0.08, 70.00],
                [115.00, 0.00, 201.00, 27.00, 0.07, 81.00],
                [116.00, 0.00, 260.00, 350.00, 0.05, 81.00],
                [191.00, 4.00, 374.00, 99.00, 0.05, 70.00],
            ]
        ),
    ]

    return gt, pred


@pytest.fixture
def three_samples_with_partially_empty_gt(coco_val2017_three_samples):
    gt, pred = coco_val2017_three_samples
    gt[0] = torch.Tensor(0, 5)
    return gt, pred


@pytest.fixture
def three_samples_with_partially_empty_pred(coco_val2017_three_samples):
    gt, pred = coco_val2017_three_samples
    pred[1] = torch.Tensor(0, 6)
    return gt, pred


@pytest.fixture
def three_partially_empty_samples(coco_val2017_three_samples):
    gt, pred = coco_val2017_three_samples
    gt[0] = torch.Tensor(0, 5)
    gt[2] = torch.Tensor(0, 5)
    pred[1] = torch.Tensor(0, 6)
    return gt, pred


@pytest.fixture
def three_other_partially_empty_samples(coco_val2017_three_samples):
    gt, pred = coco_val2017_three_samples
    gt[1] = torch.Tensor(0, 5)
    pred[1] = torch.Tensor(0, 6)
    return gt, pred


def create_coco_api(predictions, targets):
    """Create COCO object from predictions and targets

    Args:
        predictions torch.Tensor: predictions in (N, 5) shape where 5 is (x1, y1, x2, y2, score, class_id)
        targets torch.Tensor: targets in (N, 6) shape where 6 is (x1, y1, x2, y2, class_id)

    Returns:
        Tuple[coco_api.COCO, coco_api.COCO]: coco object
    """
    ann_id = 1
    coco_gt = COCO()
    dataset = {"images": [], "categories": [], "annotations": []}

    for idx, target in enumerate(targets):
        dataset["images"].append({"id": idx})
        for i in range(target.shape[0]):
            bbox = target[i][:4]
            bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
            bbox = [x.item() for x in bbox]
            area = bbox[2] * bbox[3]
            ann = {
                "image_id": idx,
                "bbox": bbox,
                "category_id": target[i][4].item(),
                "area": area,
                "iscrowd": False,
                "id": ann_id,
            }
            dataset["annotations"].append(ann)
            ann_id += 1
    dataset["categories"] = [{"id": i} for i in range(0, 100)]
    coco_gt.dataset = dataset
    coco_gt.createIndex()

    for idx, prediction in enumerate(predictions):
        prediction[:, 2:4] = prediction[:, 2:4] - prediction[:, 0:2]
        predictions[idx] = torch.cat([torch.tensor(idx).repeat(prediction.shape[0], 1), prediction], dim=1)
    predictions = torch.cat(predictions, dim=0)
    coco_dt = coco_gt.loadRes(predictions.numpy())
    return coco_gt, coco_dt


def _test_compute(predictions, targets, device, approx=1e-2):
    coco_gt, coco_dt = create_coco_api(
        [torch.clone(pred) for pred in predictions], [torch.clone(target) for target in targets]
    )
    eval = COCOeval(coco_gt, coco_dt, iouType="bbox")
    eval.evaluate()
    eval.accumulate()
    eval.summarize()

    metric_50 = MeanAveragePrecision(iou_thresholds=[0.5], device=device)
    metric_75 = MeanAveragePrecision(iou_thresholds=[0.75], device=device)
    metric_50_95 = MeanAveragePrecision(device=device)

    targets = [t.to(device) for t in targets]
    predictions = [p.to(device) for p in predictions]

    for prediction, target in zip(predictions, targets):
        metric_50.update((prediction, target))
        metric_75.update((prediction, target))
        metric_50_95.update((prediction, target))

    res_50 = metric_50.compute()
    res_75 = metric_75.compute()
    res_50_95 = metric_50_95.compute()

    assert eval.stats[0] == pytest.approx(res_50_95, abs=approx)
    assert eval.stats[1] == pytest.approx(res_50, abs=approx)
    assert eval.stats[2] == pytest.approx(res_75, abs=approx)


def test_gt_pred_all_exist(coco_val2017_three_samples):
    targets, predictions = coco_val2017_three_samples
    _test_compute(predictions, targets, torch.device("cpu"))
    if torch.cuda.is_available():
        _test_compute(predictions, targets, torch.device("cuda"), approx=1e-6)


def test_gt_partially_empty(three_samples_with_partially_empty_gt):
    targets, predictions = three_samples_with_partially_empty_gt
    _test_compute(predictions, targets, torch.device("cpu"))
    if torch.cuda.is_available():
        _test_compute(predictions, targets, torch.device("cuda"), approx=1e-6)


def test_pred_partially_empty(three_samples_with_partially_empty_pred):
    targets, predictions = three_samples_with_partially_empty_pred
    _test_compute(predictions, targets, torch.device("cpu"))
    if torch.cuda.is_available():
        _test_compute(predictions, targets, torch.device("cuda"), approx=1e-6)


def test_both_partially_empty(three_partially_empty_samples):
    targets, predictions = three_partially_empty_samples
    _test_compute(predictions, targets, torch.device("cpu"))
    if torch.cuda.is_available():
        _test_compute(predictions, targets, torch.device("cuda"), approx=1e-6)


def test_both_partially_empty_2(three_other_partially_empty_samples):
    targets, predictions = three_other_partially_empty_samples
    _test_compute(predictions, targets, torch.device("cpu"))
    if torch.cuda.is_available():
        _test_compute(predictions, targets, torch.device("cuda"), approx=1e-6)


def test_no_torchvision():
    with patch.dict(sys.modules, {"torchvision.ops": None}):
        with pytest.raises(ModuleNotFoundError, match=r"This module requires torchvision to be installed."):
            MeanAveragePrecision()
