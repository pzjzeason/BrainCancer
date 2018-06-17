<template>
<div id="pic">
  <div id="carousel" v-if="urls.length>0" style="position: relative">
    <el-carousel :autoplay="false" arrow="always" indicator-position="none" @change="pic_change($event)">
      <el-carousel-item v-for="pic in urls" :key="pic">
        <img :src=pic />
      </el-carousel-item>
    </el-carousel>
    <div style="position: absolute;top:300px;left:480px;">
      <p>{{show_words+1}}/{{Object.keys(pics).length}}</p>
    </div>
      <div id="dis" style="position: relative;overflow-y: hidden">
        <p style="overflow-y: scroll;width: auto;height: 70px;"><i>{{words[show_words][1]}}(由英文资料翻译，开启中英模式可查看原文)
          <!--<el-tooltip content="由英文资料翻译，查看原文请开启中英模式" placement="top">-->
            <!--<i class="fas fa-question" style="position: relative"></i>-->
          <!--</el-tooltip><br>-->
          <span v-show="en"><br>{{words[show_words][0]}}</span></i>
        </p>
      </div>
  </div>
  <div v-else><p style="margin-top: 200px">暂时没有图片</p></div>
</div>
</template>

<script>
import bus from "../assets/js/bus";
import md5 from "js-md5";
export default {
  name: "pic",
  data() {
    return {
      show_words: 0,
      pics: {},
      en: false,
    };
  },
  methods: {
    pic_change(event) {
      this.show_words = event;
    }
  },
  computed: {
    urls() {
      let urls = [];
      for (let pic in this.pics) {
        pic = pic.toLowerCase();
        urls.push(require("../assets/pics/" + pic + ".jpg"));
      }
      return urls;
    },
    words() {
      let words = [];
      for (let pic in this.pics) {
        words.push(this.pics[pic]);
      }
      return words;
    }
  },
  created() {
    bus.$on("first_pics", data => {
      console.log(data);
      this.pics = data;
    });
  },
  mounted() {
    bus.$on("new_pics", data => {
      this.pics = data;
    });
    bus.$on("similar_pics", data => {
      this.pics = data;
    });
    bus.$on("lang", en => {
      this.en = en;
    })
  }
};
</script>

<style >
#pic {
  width: 1000px;
  height: 400px;
  position: absolute;
  top: 60px;
  left: 430px;
  text-align: center;
  margin-top: 30px;
  border: solid 1px #ddd;
  border-radius: 0 6px 6px 6px;
  -webkit-box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  background: white;
}
#pic img {
  max-width: 400px;
  max-height: 290px;
  margin: 10px auto;
}
button.el-carousel__arrow {
  outline: none;
  font-size: 25px;
  color: black;
  height: 50px;
  width: 50px;
}
button:focus {
    outline: none !important;
}
.el-carousel__arrow--right {
  right: 100px;
}
.el-carousel__arrow--left {
  left: 100px;
}
.el-tabs--border-card
  > .el-tabs__header
  .el-tabs__item:not(.is-disabled):hover {
  color: black;
}
#dis {
  margin: 20px auto;
  width: 700px;
}
#words_en {
  z-index: 60;
  position: absolute;
  width: 500px;
  max-height: 100px;
  background: white;
  top: 0;
  left: 100px;
  border-radius: 10px;
  overflow-y: scroll;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
  border: #adb5bd solid 1px;
}
</style>
