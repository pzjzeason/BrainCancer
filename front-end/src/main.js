// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import myheader from "./components/myheader";
import mycontent from "./components/mycontent";
import pic from "./components/pic";
import mynav from "./components/mynav";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import {
  Switch,
  Tree,
  Tabs,
  TabPane,
  Carousel,
  CarouselItem,
  MessageBox,
  Message,
  Tooltip,
  Dialog
} from "element-ui";
Vue.prototype.$http = axios;
Vue.component(Switch.name,Switch);
Vue.component(Tree.name,Tree);
Vue.component(Tabs.name,Tabs);
Vue.component(TabPane.name,TabPane);
Vue.component(Carousel.name,Carousel);
Vue.component(CarouselItem.name,CarouselItem);
Vue.component(MessageBox.name,MessageBox);
Vue.component(Tooltip.name,Tooltip);
Vue.component(Dialog.name,Dialog);


Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$message = Message;

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: "#header",
  render: h => h(myheader),
  components: { myheader },
  template: "<myheader/>"
});
new Vue({
  el: "#nav",
  render: h => h(mynav),
  components: { mynav },
  template: "<mynav/>"
});
new Vue({
  el: "#pic",
  render: h => h(pic),
  components: { pic },
  template: "<pic/>"
});
new Vue({
  el: "#content",
  render: h => h(mycontent),
  components: { mycontent },
  template: "<mycontent/>"
});
