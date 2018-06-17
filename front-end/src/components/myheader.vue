<template>
  <div  style="border-bottom: solid black 3px">
    <h1 style="margin-left: 50px; ">BrainCancer</h1>
    <div >
      <el-switch
        v-model="en"
        active-text="中英"
        inactive-text="中文"
        active-color="#6c757d"
        inactive-color= "#cccccc">
      </el-switch>
    </div>
    <span id="pre"  @click="dialogTableVisible = true">演示<i class="fas fa-mouse-pointer fa-xs"></i></span>
    <el-dialog title="演示" :visible.sync="dialogTableVisible" @close="stop">
      <video id="video" width="700" controls poster="../assets/poster.png" :key="key">
        <source  src="../assets/pre.mp4" type="video/mp4"/>
      </video>
</el-dialog>
  </div>
</template>

<script>
import bus from "../assets/js/bus";
export default {
  name: "HelloWorld",
  data() {
    return {
      en: false,
      dialogTableVisible: false,
      key: 0
    };
  },
  watch: {
    en() {
      bus.$emit("lang", this.en);
    }
  },
  methods: {
    stop() {
      let video = document.querySelector("#video");
      console.log('stop playing video');
        video.pause();
        video.currentTime = 0;
        this.key += 1
    }
  }
};
</script>

<style >
.el-switch {
  position: absolute;
  color: #adb5bd;
  top: 20px;
  left: 300px;
}
.el-switch__label {
  color: #adb5bd;
}
.el-switch__label.is-active {
  color: black;
}
#pre {
  position: absolute;
  top: 18px;
  left: 450px;
  cursor: pointer;
}
.el-dialog__wrapper {
  text-align: center;
}
.el-dialog {
  width: 800px;
}
.el-dialog__body {
  padding: 0;
}
</style>
