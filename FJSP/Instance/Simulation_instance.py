'''
实验数据来自论文：唐亮，程峰，吉卫喜，金志斌．改进 ICA 求解柔性作业车间插单重调度问题[J/OL]．计算机工程与应用.
'''

#加工机器
MT=[
    [
        [1,2,3,4,5,7,8],
        [1,3,4,5,6,7,8],
        [2,4,5,6,7,8]
    ],
    [
        [1,2,3,4,5,7],
        [2,3,4,5,6,7,8],
        [2,4,5,6,7,8],
        [1,2,3,4,6,8]
    ],
    [
        [1,4,5,6,7,8],
        [2,3,4,5,6,7],
        [1,2,3,4,6,8],
    ],
    [
        [1,2,3,4,5,6,7,8],
        [1,2,3,4,5,6,7,8],
        [1,2,3,4,5,6,7,8],
    ],
    [
        [1,2,3,4,5,7],
        [1, 3, 4, 5,6, 7],
        [2,3,4,5,6,7],
        [1,2,4,5,6,7,8]
    ],
    [
        [1,2,3,4,5,6,8],
        [1,3,4,5,6,7,8],
        [1,2,3,4,5,7]
    ],
    [
        [1,2,3,4,5,7],
        [2,3,4,5,6,8],
        [2,3,4,5,6,8]
    ],
    [
        [1,2,3,4,6,8],
        [1,2,3,4,5,7],
        [1,2,4,5,6,7,8],
        [1,3,4,5,6,7],
    ],
    [
        [1,3,4,5,6,7],
        [2,3,5,6,7,8],
        [1,2,4,5,6,7]
    ]
]

#加工时间
PT=[
    [
[5,3,5,3,3,10,9],
[10,5,8,3,9,9,6],
[10,5,6,2,4,5]
    ],
    [
[5,7,3,9,8,9],
[8,5,2,6,7,10,9],
[10,5,6,4,1,7],
[1,4,5,6,10,7],
    ],
    [
[10,7,6,5,2,4],
[10,6,4,8,9,10],
[1,4,5,6,10,7],
    ],
    [
[3,1,6,5,9,7,8,4],
[12,11,7,8,10,5,6,9],
[4,6,2,10,3,9,5,7],
    ],
    [
[3,6,7,8,9,10],
[10,7,4,9,8,6],
[9,8,7,4,2,7],
[11,9,6,7,5,3,6]
    ],
    [
[6,7,1,4,6,9,10],
[11,9,9,9,7,6,4],
[10,5,9,10,11,10],
    ],
    [
[5,4,2,6,7,10],
[9,9,11,9,10,5],
[8,9,3,8,6,10],
    ],
    [
[2,8,5,9,4,10],
[7,4,7,8,9,10],
[9,9,8,5,6,7,1],
[9,3,7,1,5,8],
    ],
    [
[9,5,2,3,5,3],
[8,5,6,2,4,3],
[8,6,3,5,5,2],
    ],
]

#能耗
EC=[
    [
[1.6,1.8,2.4,2.2,3.5,2.4,2.7],
[2.4,2,1.6,2.7,1.8,1.6,2.2],
[1.8,2.4,1.6,2.7,3.5,2.8],
    ],
    [
[1.6,2,2.2,1.8,2.8,2.4],
[1.8,2.4,2,3.5,2.8,4.1,2.7],
[1.8,1.6,2.4,4.1,2.8,1.6],
[2.8,1.8,2.2,2.4,2.7,3.1],
    ],
    [
[2.2,1.8,2.4,2.7,2.4,2.8],
[2.4,1.8,2.2,1.6,3.2,2.2],
[2.2,2.7,2.4,1.8,2.6,1.8],
    ],
    [
[2.2,2.4,2.6,1.8,2.4,3.5,2.8,2.4],
[2.4,2.2,2.6,1.8,3.1,2,3.5,2.7],
[2.8,2.5,2.6,2.4,2.8,1.8,2.2,2.5],
    ],
    [
[2.2,2.6,2.4,3.5,4.1,2],
[1.8,2.4,2.2,2.6,3.1,2.7],
[3.1,2.6,2.8,2.4,2.6,3.5],
[2.2,2.6,3.1,1.8,2.4,2.2,2.8],
    ],
    [
[2.8,2.2,2.6,2.3,3.4,2.8,3.1],
[2.4,1.8,3.1,2.2,3.5,2.2,2.6],
[2.6,2.4,3.1,2.2,2.7,2.5],
    ],
    [
[2.6,2.2,2.4,3.1,2.8,2.5],
[2.8,2.6,2.2,2.6,3.3,2.4],
[2.6,2.4,2.8,1.8,3.5,4.1],
    ],
    [
[2.6,2.4,3.1,1.8,2.2,2],
[2.5,2.8,3.1,2.2,2.6,3.1],
[2.2,2.5,3.1,2.4,1.8,3.5,2.6],
[2.6,2.2,3.1,2.4,2.8,3.5],
    ],
    [
[2.7,2.4,2.6,3.1,2.5,1.8],
[1.8,2.4,2.6,2.2,3.5,2.8],
[3.1,2.4,2.2,2.8,2.6,4.1],
    ],
]

# Equipment standby power consumption
ESPC=[0.6,0.6,0.3,0.4,0.4,0.4,0.6,0.8,0.9]

n, m=9,8
ni=[3,4,3,3,4,3,3,4,3]