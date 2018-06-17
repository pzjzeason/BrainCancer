<template>
  <div id="mycontent">
    <div style="height: 30px;position: relative">
      <i class="fas fa-arrow-left" style="top: 3px" :class="[current>0 ? 'active_icon':'fake_icon']"  @click="history(-1)"></i><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <i class="fas fa-arrow-right" style="top: 3px" :class="[current<this.visited.length-1 ? 'active_icon':'fake_icon']" @click="history(1)"></i><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <i class="fab fa-wikipedia-w" id="wiki" @click="wiki"></i>
      <img id="baidu" src="../assets/icons/baidu.png" style="position: absolute" @click="baidu"/>
      <img id="xueshu" src="../assets/icons/xueshu.png" style="position: absolute" @click="xueshu"/>
    </div>
    <el-tabs type="border-card" v-if="content['NameInCN']" v-model="active_tab">
      <el-tab-pane label="基本资料" name="first">
        <div class="content_pane">
          <br>
          <ul>
            <li class="title">
              中文名称:
            </li>
            <li class="info">
              {{content['NameInCN'][0]}}
            </li>
            <li class="title">
              英文名称:
            </li>
            <li class="info">
              {{content['tumorNameEn']}}
            </li>
          </ul>
          <ul>
            <li class="title">
              中文别名:
            </li>
            <li class="info">
              <span v-for="name in content['nameAlsoCn']">{{name}}&nbsp&nbsp&nbsp&nbsp</span>
            </li>
            <li class="title">
              英文别名:
            </li>
            <li class="info" style="width: 300px">
              <span v-for="name in content['nameAlsoEn']">{{name}}&nbsp&nbsp&nbsp&nbsp</span>
            </li>
          </ul>
          <ul>
            <li class="title">
              ICD-O编码:
            </li>
            <li class="info">
              {{content['ICD_OCode'][0]}}
            </li>
            <li class="title">
              ICD-10编码:
            </li>
            <li class="info">
              {{content['ICD_10Code'][0]}}
            </li>
          </ul>
          <ul>
            <li class="title">
              Mesh编码:
            </li>
            <li class="info">
              {{content['MeshCode'][0]}}
            </li>
            <li class="title" style="width: 120px">
              ICD-10主题词:
            </li>
            <li class="info" style="width: 400px">
              {{content['ICDThematicWord'][0]}}
            </li>
          </ul>
          <ul>
            <li class="title">
              Mesh主题词:
            </li>
            <li class="info">
              {{content['MeshThematicWord'][0]}}
            </li>
            <li class="title">
              疾病定义:
            </li>
            <li v-if="content['definitionCn'][0]!=='暂缺'||content['definitionEn'][0]!=='暂缺'" class="info" style="width: 400px">
              <span v-show="content['definitionCn'][0]!=='暂缺'">{{content['definitionCn'][0]}}<br><br></span>
              <i v-show="content['definitionEn'][1]!=='暂缺'">{{content['definitionEn'][1]}}(由英文资料翻译，开启中英模式可查看原文)</i><br><br>
              <i v-show="en&&content['definitionEn'][1]!=='暂缺'">{{content['definitionEn'][0]}}</i>
            </li>
            <li v-else class="info">暂缺</li>
          </ul>
          </div>
    </el-tab-pane>
    <el-tab-pane label="疾病特征" name="second">
      <div class="content_pane">
        <br>
      <ul>
        <li class="title">发病率:</li>
        <li class="info">{{content['OccurrenceRate'][1]}}</li>
        <li class="title">易发人群:</li>
        <li v-if="content['hasFindingSite'][0]!=='暂缺'" class="info"><span v-for="each in content['hasHighOccurrenceRateIn']">{{each[1]}}<span v-show="en">({{each[0]}})</span>&nbsp&nbsp&nbsp</span></li>
        <li v-else class="info">暂缺</li>
      </ul>
      <ul>
        <li class="title"><span>易发脑区:</span></li>
        <li v-if="content['hasFindingSite'][0]!=='暂缺'" class="info" style="width: 800px"><span v-for="each in content['hasFindingSite']"> <span @click="open(each[0])" class="ass">{{each[1]}}<span v-show="en">({{each[0]}})</span><i class="fas fa-mouse-pointer fa-xs"></i></span>&nbsp&nbsp&nbsp&nbsp</span></li>
        <li v-else class="info">暂缺</li>
      </ul>
      <ul>
        <li class="title">临床表现:</li>
        <li v-if="content['hasFindingSite'][0]!=='暂缺'" class="info" style="width: 800px"><span v-for="each in content['hasSymptoms']">{{each[1]}}<span v-show="en">({{each[0]}})</span>&nbsp&nbsp&nbsp</span></li>
        <li v-else class="info">暂缺</li>
      </ul>
      <ul >
        <li class="title">病因:</li>
        <li v-if="content['PathogenyInCN'][0]!=='暂缺'||content['Pathogeny'][0]!=='暂缺'" class="info" style="width: 800px"><span v-show="content['PathogenyInCN'][0]!=='暂缺'">{{content['PathogenyInCN'][0]}}<br><br></span>
          <i v-show="content['Pathogeny'][1]!=='暂缺'">{{content['Pathogeny'][1]}}(由英文资料翻译，开启中英模式可查看原文)</i><br><br>
          <i v-show="en&&content['Pathogeny'][1]!=='暂缺'">{{content['Pathogeny'][0]}}</i>
        </li>
        <li v-else class="info">暂缺</li>
      </ul>
      </div>
    </el-tab-pane>
    <el-tab-pane label="辅助诊断" name="third">
      <div class="content_pane">
        <br>
        <ul>
        <li class="title">相似肿瘤:</li>
        <!--<li class="info" style="width: 800px">{{content['associatedTumours']}}</li>-->
        <li class="info" style="width: 800px">
          <span v-if="tumor['name']" v-for="tumor in content['associatedTumours']"><el-tooltip :content="types[tumor['type']]" placement="top"><span class="ass" :class="{'cal':tumor['type']===1,'infer':tumor['type']===2}"  @click="get_similar($event.target.id)" :id="tumor['id']">{{tumor['name'][1]}}<span v-show="en">({{tumor['name'][0]}})</span><i class="fas fa-mouse-pointer fa-xs"></i></span></el-tooltip>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>
        </li>
      </ul>
      <ul>
        <li class="title">治疗项目:</li>
        <li v-if="content['isDiagnosedBy'][0]!=='暂缺'" class="info" style="width: 500px"><span v-for="each in content['isDiagnosedBy']">{{each[1]}}<span v-show="en">({{each[0]}})</span>&nbsp&nbsp&nbsp</span></li>
        <li v-else class="info">暂缺</li>
      </ul>
      <ul>
        <li class="title">鉴别诊断:</li>
        <li v-if="content['DifferentialDiagnosisInCN'][0]!=='暂缺'||content['DifferentialDiagnosis'][0]!=='暂缺'" class="info" style="width: 800px"><span v-show="content['DifferentialDiagnosisInCN'][0]!=='暂缺'">{{content['DifferentialDiagnosisInCN'][0]}}<br><br></span>
          <i v-show="content['DifferentialDiagnosis'][1]!=='暂缺'">{{content['DifferentialDiagnosis'][1]}}(由英文资料翻译，开启中英模式可查看原文)</i><br><br>
          <i v-show="en&&content['DifferentialDiagnosis'][1]!=='暂缺'">{{content['DifferentialDiagnosis'][0]}}</i>
        </li>
        <li v-else class="info">暂缺</li>
      </ul>
      </div>
    </el-tab-pane>
    <el-tab-pane label="影像描述" bane="fourth">
      <div class="content_pane">
        <br>
      <ul>
        <li class="title">核磁共振:</li>
        <li v-if="content['MRIImageDescriptionInCN'][0]!=='暂缺'||content['MRIImageDescription'][0]!=='暂缺'" class="info" style="width: 800px"><span v-show="content['MRIImageDescriptionInCN'][0]!=='暂缺'">{{content['MRIImageDescriptionInCN'][0]}}<br><br></span>
          <i v-show="content['MRIImageDescription'][1]!=='暂缺'">{{content['MRIImageDescription'][1]}}(由英文资料翻译，开启中英模式可查看原文)</i><br><br>
          <i v-show="en&&content['MRIImageDescription'][1]!=='暂缺'">{{content['MRIImageDescription'][0]}}</i>
        </li>
        <li v-else class="info">暂缺</li>
      </ul>
      <ul>
        <li class="title">CT:</li>
        <li v-if="content['CTImageDescriptionInCN'][0]!=='暂缺'||content['CTImageDescription'][0]!=='暂缺'" class="info" style="width: 800px"><span v-show="content['CTImageDescriptionInCN'][0]!=='暂缺'">{{content['CTImageDescriptionInCN'][0]}}<br><br></span>
          <i v-show="content['CTImageDescription'][1]!=='暂缺'">{{content['CTImageDescription'][1]}}(由英文资料翻译，开启中英模式可查看原文)</i><br><br>
          <i v-show="en&&content['CTImageDescription'][1]!=='暂缺'">{{content['CTImageDescription'][0]}}</i>
        </li>
        <li v-else class="info">暂缺</li>
      </ul>
      </div>
    </el-tab-pane>
      <el-tab-pane label="参考文献" bane="fifth">
        <div class="content_pane">
          <br>
          <ul>
            <li class="title" style="width: 140px">中文参考文献:</li>
            <li v-if="content['referencesCn'][0]!=='暂缺'" class="info" style="width: 800px;">
              <span v-for="each in content['referencesCn']" @click="refer_cn(each)" style="cursor: pointer;color: #d86e6e">
                <span v-if="each.split('.')[1]==='link'">{{each.split('.')[0]}}.参考链接<i class="fas fa-mouse-pointer fa-xs"></i><br/><br/></span>
                <span v-else>{{each}}<i class="fas fa-mouse-pointer fa-xs"></i><br/><br/></span>
              </span>
            </li>
            <li v-else class="info">暂缺</li>
          </ul>
          <ul>
            <li class="title" style="width: 140px">英文参考文献:</li>
            <li v-if="content['referencesEn'][0]!=='暂缺'" class="info" style="width: 800px">
              <span v-for="each in content['referencesEn']" @click="refer(each.split('.')[2])"
                    style="cursor: pointer;color: #d86e6e" v-if="each!==''">
                {{each}}<i class="fas fa-mouse-pointer fa-xs"></i><br/><br/>
              </span>
            </li>
            <li v-else class="info">暂缺</li>
          </ul>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import bus from "../assets/js/bus";
export default {
  name: "App",
  data() {
    return {
      alert: false,
      c: { T: "hhh" },
      content: {},
      en: false,
      types:['文献中显示与该肿瘤相似','计算表明与该肿瘤相似','推理得出与该肿瘤相似'],
      active_tab: 'first',
      visited:['tumor_child_3'],
      current:0,
    };
  },
  created() {
    bus.$on("first_content", data => {
      this.content = data;
    });
  },
  mounted() {
    bus.$on("new_content", data => {
      this.active_tab='first';
      this.content = data;
    });
    bus.$on("lang", en => {
      this.en = en;
    });
    bus.$on('visit',data=>{
      this.visited = this.visited.slice(0,this.current+1);
      this.current +=1;
      this.visited.push(data)
    })
  },
  methods: {
    history(type){
      if((type===-1&&this.current>0)||(type===1&&this.current<this.visited.length-1)){
        this.current +=type;
        let id = this.visited[this.current];
        console.log("get visited: " + id);
        this.$http({
          method: "get",
          url: "http://13.230.184.147:5200/" + id,
          responseType: "json"
        })
          //接收到json格式的数据
          .then(response => {
            this.active_tab='first';
            let tumor_info = response.data;
            this.content = tumor_info["content"];
            //将数据传递给影像组件和内容组件
            bus.$emit("similar_pics", tumor_info["pics"]);
            bus.$emit("similar_nav", id);
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    wiki(){
      window.open('https://en.wikipedia.org/wiki/'+this.content['tumorNameEn'].split(',')[0])
    },
    baidu(){
      window.open('https://baike.baidu.com/item/'+this.content['NameInCN'][0].split(',')[0])
    },
    xueshu(){
      window.open('https://xueshu.baidu.com/s?wd='+this.content['NameInCN'][0].split(',')[0])
    },
    refer(q){
      window.open('https://xueshu.baidu.com/s?wd='+q)
    },
    refer_cn(q){
      if(q.split('.')[1]==='link'){
        window.open(q.split('.').slice(2).join('.'))
      }
      else{
        window.open('https://xueshu.baidu.com/s?wd='+q.split('.')[2])
      }
    },
    open(area) {
      const h = this.$createElement;
      this.$msgbox({
        title: "该脑区其他肿瘤",
        message: h("div", { style: "height 200px" }, [
          h(
            "ul",
            { style: "color: teal" },
            this.content["areas"][area].map(item => {
              let m = this;
              if (item !== "hhh") {
                return h(
                  "li",
                  {
                    on: {
                      click() {
                        console.log(item);
                        m.$msgbox.close();
                        m.get_similar(item["id"]);
                      }
                    },
                    class: "msg"
                  },
                  item["name"]
                );
              }
            })
          )
        ]),
        confirmButtonText: "确定"
      });
    },
    get_similar(id) {
      this.visited = this.visited.slice(0,this.current+1);
      this.visited.push(id);
      this.current+=1;
      console.log("get similar tumor info of: " + id);
      //调用axiso与后端进行通信
      this.$http({
        method: "get",
        url: "http://13.230.184.147:5200/" + id,
        responseType: "json"
      })
        //接收到json格式的数据
        .then(response => {
          this.active_tab='first';
          let tumor_info = response.data;
          this.content = tumor_info["content"];
          //将数据传递给影像组件和内容组件
          bus.$emit("similar_pics", tumor_info["pics"]);
          bus.$emit("similar_nav", id);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style>
#mycontent {
  margin-top: 20px;
  width: 1000px;
  height: 280px;
  position: absolute;
  top: 470px;
  left: 430px;
}
#mycontent .active_icon{
  cursor: pointer;
}
#mycontent .fake_icon{
  color: #cccccc;;
}
#mycontent #baidu{
  position: absolute;
  height: 20px;
  top: 5px;
  left: 120px;
  cursor: pointer;
}
#mycontent #wiki{
  position: absolute;
  height: 20px;
  top: 8px;
  left: 85px;
  cursor: pointer;
  color: black;
  font-weight: 500;
}
#mycontent #xueshu{
  position: absolute;
  height: 30px;
  left: 150px;
  cursor: pointer;
}
#mycontent .content_pane {
  height: 250px;
  overflow-y: scroll;
}
#mycontent .el-tabs--border-card {
  border-radius: 10px;
  height: 300px;
}
#mycontent .el-tabs--border-card > .el-tabs__header .el-tabs__item.is-active {
  color: black;
}
.el-tabs--border-card > .el-tabs__content {
  padding: 0;
}
.col-1 {
  width: 60px;
}
#mycontent li {
  display: inline-table;
}
.title {
  width: 100px;
  font-weight: 700;
}
.info {
  width: 250px;
  font-weight: 400;
}
#mycontent .ass {
  display: inline-table;
  cursor: pointer;
  color: #d86e6e;
}
#mycontent .cal {
  color: teal;
}
#mycontent .infer {
  color: gold;
}
.el-message-box__content {
  height: 200px;
  overflow-y: scroll
}
li.msg {
  cursor: pointer;
}
li.msg:hover {
  color: #d86e6e;
}
.el-button--primary {
  color: #fff;
  background-color: #6c757d;
  border: none;
}
.el-button--primary:hover {
  background: teal;
  color: #fff;
}
  .fa, .fas {
    font-weight: 900;
    position: relative;
    left: 3px;
}
</style>
