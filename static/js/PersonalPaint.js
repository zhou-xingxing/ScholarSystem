var data = {
        value: [
          {
            "name": "清华大学",
            "value": 309
          },
          {
            "name": "人工智能",
            "value": 260
          },
          {
            "name": "无人驾驶",
            "value": 173
          },
          {
            "name": "深度学习",
            "value": 155
          },
          {
            "name": "卷积神经网络",
            "value": 3360
          },
          {
            "name": "ACM fellow",
            "value": 121
          },
          {
            "name": "计算机系",
            "value": 76
          },
          {
            "name": "计算机图形学",
            "value": 62
          },
          {
            "name": "教授",
            "value": 37
          },
          {
            "name": "EMNLP",
            "value": 32
          },
          {
            "name": "学术成果丰富",
            "value": 28
          },
          {
            "name": "合作人员众多",
            "value": 4
          },
          {
            "name": "百度CTO",
            "value": 1275
          },
          {
            "name": "AI LAB",
            "value": 254
          },
          {
            "name": "姚期智",
            "value": 188
          },
          {
            "name": "唐杰",
            "value": 166
          },
          {
            "name": "正直",
            "value": 942
          },
          {
            "name": "友善",
            "value": 177
          },
          {
            "name": "聪明",
            "value": 133
          },
          {
            "name": "美发",
            "value": 80
          },
          {
            "name": "香水",
            "value": 50
          },
          {
            "name": "个人护理",
            "value": 46
          },
          {
            "name": "美甲",
            "value": 26
          },
          {
            "name": "SPA美体",
            "value": 21
          },
          {
            "name": "ICCV 5篇",
            "value": 914
          },
          {
            "name": "绿植花卉",
            "value": 311
          },
          {
            "name": "狗",
            "value": 257
          },
          {
            "name": "其他宠物",
            "value": 131
          },
          {
            "name": "水族",
            "value": 125
          },
          {
            "name": "猫",
            "value": 122
          },
          {
            "name": "动物",
            "value": 81
          },
          {
            "name": "鸟",
            "value": 67
          },
          {
            "name": "宠物用品",
            "value": 41
          },
          {
            "name": "宠物服务",
            "value": 26
          },
          {
            "name": "图像识别",
            "value": 913
          },
          {
            "name": "路障检测",
            "value": 483
          },
          {
            "name": "面相分析",
            "value": 47
          },
          {
            "name": "手相",
            "value": 32
          },
          {
            "name": "公益",
            "value": 90
          }
        ],
        //专家图片，转码成base64
          image:"data:image/png;base64,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"
      }
      $(function() {
          var myChart = echarts.init(document.getElementById('7_main'));
          //温馨提示：image 选取有严格要求不可过大；，否则firefox不兼容 iconfont上面的图标可以
          var maskImage = new Image();
          maskImage.src = data.image

          maskImage.onload = function(){
              myChart.setOption( {
              backgroundColor:'#fff',
              tooltip: {
                show: false
              },
              series: [{
                type: 'wordCloud',
                gridSize: 1,
                sizeRange: [12, 55],
                rotationRange: [-45, 0, 45, 90],
                maskImage: maskImage,
                textStyle: {
                  normal: {
                    color: function() {
                      return 'rgb(' +
                          Math.round(Math.random() * 255) +
                          ', ' + Math.round(Math.random() * 255) +
                          ', ' + Math.round(Math.random() * 255) + ')'
                    }
                  }
                },
                left: 'center',
                top: 'center',
                // width: '96%',
                // height: '100%',
                right: null,
                bottom: null,
                // width: 300,
                // height: 200,
                // top: 20,
                data: data.value
              }]
            })
          }
      })


