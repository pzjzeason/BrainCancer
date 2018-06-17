<template>
<div id="mynave">
  <div class="container">
    <div class="row" style="width: 80%; margin: auto">
        <div class="input-group">
          <div class="input-group-btn">
            <button type="button" class="btn btn-secondary dropdown-toggle"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              {{ search_entry }}
            </button>
            <div class="dropdown-menu">
              <a class="dropdown-item" @click="search_entry='名称'">名称</a>
              <a class="dropdown-item" @click="search_entry='name'">name</a>
              <a class="dropdown-item" @click="search_entry='icd'">icd</a>
              <a class="dropdown-item" @click="search_entry='mesh'">mesh</a>
            </div>
          </div>
          <input type="text" class="form-control" placeholder="Search here" aria-label="Text input with dropdown button"
                 @blur="hide_result" v-on:keyup.enter="search" v-model="search_key">
          <i class="fas fa-search fa-lg" style="position: absolute; top: 10px; left: 280px;z-index: 60"></i>
        </div>
    </div>
    <div id="navs">
      <h4>
        <span id="bla" :class="common_or_who===1?'':'hide'" @click="to_common">常见</span>&nbsp;&nbsp;|&nbsp;&nbsp;
        <span :class="common_or_who===2?'':'hide'" @click="to_who">WHO</span>&nbsp;&nbsp;|&nbsp;&nbsp;
        <span :class="common_or_who===3?'':'hide'" @click="to_brain">脑区</span>
      </h4>
    </div>
    <div v-show="common_or_who===1">
      <el-tree
        ref="tree2"
        :data=common
        node-key="id"
        :highlight-current=true
        :props="defaultProps"
        @node-click="select_from_common()"
        :accordion= true
      >
      </el-tree>
    </div>
    <div v-show="common_or_who===2" class="tree">
      <el-tree
        ref="tree"
        :data="who"
        node-key="id"
        :highlight-current=true
        :props="defaultProps"
        :default-expanded-keys=expand
        @node-click="select_from_nav()"
        :accordion= true
        :key = "k"
      >
      </el-tree>
    </div>
    <div v-show="common_or_who===3" class="tree">
      <el-tree
        ref="tree3"
        :data="brain"
        node-key="id"
        :highlight-current=true
        :props="defaultProps"
        :default-expanded-keys=expand_brain
        @node-click="select_from_brain()"
        :accordion= true
      >
      </el-tree>
    </div>
    <div class="list-group"  v-show=show_result>
      <a v-for="item in result" v-html="item['html']" :id = "item['id']" @click= "select_from_search($event)"
         class="list-group-item list-group-item-action"
      >
      </a>
    </div>
  </div>
</div>
</template>

<script>
import bus from "../assets/js/bus";
import lodash from 'lodash'
export default {
  name: "mynav",
  data: function() {
    return {
      search_entry: "名称",
      search_key: "",
      common: [],
      who: [],
      brain:[],
      common_or_who: 1,
      current_common: "tumor_child_3",
      current_who: "tumor_child_0",
      current_brain:"tumor_child_3",
      expand: ["tumor_parent_0"],
      expand_brain: ["brain_parent_0"],
      k: "tumor_child_0",
      result: {},
      show_result: false,
      pics: [],
      defaultProps: {
        children: "children",
        label: "label"
      }
    };
  },
  methods: {
    to_common(){
      this.common_or_who = 1;
      this.get_tumor_info(this.current_common)
    },
    to_who(){
      this.common_or_who = 2;
      this.get_tumor_info(this.current_who)
      // this.current_who = this.current_common;
      // this.expand = [this.current_who];
      // this.$refs.tree.setCurrentKey(this.current_who);
      // this.k = this.current_who;
    },
    to_brain(){
      this.common_or_who = 3;
      this.get_tumor_info(this.current_brain)
    },
    search: function() {
      if(this.search_key===''){
        this.result=[{'id': 'null', 'html': '正在输入...'}];
      }
      else {
        this.$http({
          method: "post",
          url: "http://13.230.184.147:5200/search",
          data: [this.search_entry, this.search_key],
          responseType: "json"
        })
          .then(response => {
            console.log(response.data);
            this.result = response.data;
            this.show_result = true;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    hide_result(){
      setTimeout(()=>{this.show_result = false},500)
    },
    get_tumor_info: function(id) {
      bus.$emit('visit', id);
      console.log("get info of: " + id);
      //调用axiso与后端进行通信
      this.$http({
        method: "get",
        url: "http://13.230.184.147:5200/" + id,
        responseType: "json"
      })
        //接收到json格式的数据
        .then(response => {
          let tumor_info = response.data;
          console.log(tumor_info);
          //将数据传递给影像组件和内容组件
          bus.$emit("new_pics", tumor_info["pics"]);
          bus.$emit("new_content", tumor_info["content"]);
        })
        .catch(error => {
          console.log(error);
        });
    },
    select_from_common(){
      let id = this.$refs.tree2.getCurrentKey();
      this.current_common = id;
      this.get_tumor_info(id);
    },
    select_from_nav() {
      let id = this.$refs.tree.getCurrentKey();
      this.current_who = id;
      this.expand = [id];
      if (id[6] !== "p") {
        this.get_tumor_info(id);
        console.log("select child from tree: " + id);
      } else console.log("select parent node");
    },
    select_from_brain() {
      let id = this.$refs.tree3.getCurrentKey();
      this.current_brain = id;
      this.expand_brain = [id];
      if (id[6] !== "p") {
        this.get_tumor_info(id);
        console.log("select child from tree: " + id);
      } else console.log("select parent node");
    },
    select_from_search(event) {
      this.common_or_who=2;
      let id = event.currentTarget.id;
      this.expand = [id];
      this.current_who = id;
      this.get_tumor_info(id);
      console.log("select from search: " + id);
      this.k = id;
    },
    change: function() {
      this.common_or_who = 2;
    }
  },
  watch: {
    current_who: function() {
      this.$refs.tree.setCurrentKey(this.current_who);
    },
    search_key:function (oldval,newval) {
      this.result=[{'id': 'null', 'html': '正在输入...'}];
      this.show_result=true;
      this.debouncedGetAnswer()
    }
  },
  created: function () {
    this.$http({
      method: "get",
      url: "http://13.230.184.147:5200/tree",
      data: "get tree data",
      responseType: "json"
    })
      .then(response => {
        this.common = response.data[0];
        this.who = response.data[1];
        this.brain = response.data[2];
        console.log("received tree data");
        // bus.$emit("new_pics", tumor_info['pics']);
        // bus.$emit("new_content", tumor_info['content']);
      })
      .catch(error => {
        console.log(error);
      });
    this.$http({
      method: "get",
      url: "http://13.230.184.147:5200/tumor_child_3",
      data: "get tumor information",
      responseType: "json"
    })
      .then(response => {
        let tumor_info = response.data;
        console.log("received default child data");
        console.log(tumor_info);
        bus.$emit("first_pics", tumor_info["pics"]);
        bus.$emit("first_content", tumor_info["content"]);
      })
      .catch(error => {
        console.log(error);
      });
    this.debouncedGetAnswer = lodash.debounce(this.search, 500)
  },
  mounted(){
    bus.$on('similar_nav',id=>{
      this.current_who = id;
      this.common_or_who = 2;
      this.expand = [this.current_who];
      this.k=this.current_who
    })
  },
  updated: function() {
    this.$refs.tree2.setCurrentKey(this.current_common);
    this.$refs.tree.setCurrentKey(this.current_who);
    this.$refs.tree3.setCurrentKey(this.current_brain);
  }
};
</script >

<style>
#mynave {
  width: 430px;
  height: 700px;
  margin-top: 30px;
}
#mynave .form-control:focus {
  box-shadow: none;
}
#mynave h4 {
  text-align: center;
  margin-top: 25px;
}
#mynave ul {
  text-align: center;
  font-size: 20px;
  padding: 0;
  list-style-position: inside;
}
#mynave a{
  cursor: pointer;
}
#mynave .hide {
  color: #999999;
  cursor: pointer;
}
#mynave .little {
  font-size: 15px;
}
#mynave .list-group {
  position: absolute;
  top: 130px;
  left: 130px;
  min-width: 250px;
  z-index: 50;
}
.tree{
  overflow-y: scroll;height: 600px
}
.el-tree-node__content {
  height: 35px;
}
.el-tree-node__label {
  font-size: 15px;
}
.is-current .el-tree-node__label {
  font-size: 15px;
  color: black;
  font-weight: 500;
}
.el-tree-node__expand-icon {
  font-size: 25px;
}
.el-tree-node__children .el-tree-node__label {
  font-size: 15px;
}
  .el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content {
    background-color: rgba(31,45,61,.11);
}
</style>
