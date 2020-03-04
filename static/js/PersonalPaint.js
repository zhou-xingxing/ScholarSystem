var paper_key=data.paper_search_key;
var paper_num =data.paper_search_num;
var scholar_school=data.scholar_school;
var scholar_name=data.scholar_name;
var labels=[];  //个人画像的标签，目前考虑到的有：论文关键词、工作机构、学科专业、
var max_value=0; //这里是为了取到关键词的最大value值，然后赋给学者姓名。
// 可能会因为太大，而背景尺寸太小字数无法显示。需要修改64行的width和height。 ---2020.3.4 bwm

for (i=0,len=paper_key.length;i<len;i++){
            labels.push({
                "name": paper_key[i],
                "value": paper_num[i],
            });
            if (paper_num[i]>max_value){
                max_value=paper_num[i]
            };
        }
labels.push({
  "name":scholar_school,
  "value":1,
});
labels.push({
  "name":scholar_name,
  "value":max_value,
});

var data1 = {
  value: labels,
        //专家图片，转码成base64
  image:"data:image/png;base64,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"
      }
      $(function() {
          var myChart = echarts.init(document.getElementById('7_main'));
          //温馨提示：image 选取有严格要求不可过大；，否则firefox不兼容 iconfont上面的图标可以
          var maskImage = new Image();
          maskImage.src = data1.image

          maskImage.onload = function(){
              myChart.setOption( {
              backgroundColor:'#fff',
              tooltip: {
                show: false
              },
              series: [{
                type: 'wordCloud',
                gridSize: 5,  //用来调制字的大小范围
                sizeRange: [12,45],  //用来调制词的旋转方向
                rotationRange: [-45, 0, 45, 90],  //生成字体颜色选择
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
                width: '100%',
                height: '100%',
                right: null,
                bottom: null,
                //width: 400,
                //height: 400,
                // top: 20,
                data: data1.value
              }]
            })
          }
      })


