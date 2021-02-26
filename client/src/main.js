import { createApp } from 'vue'
import App from './App.vue'
// import * as CanvasJs from 'canvasjs';
import BaseBlock from "./UI/BaseBlock.vue";
import CircleButton from "./UI/CircleButton.vue";

const app = createApp(App);
app.component('base-block', BaseBlock)
app.component('circle-button', CircleButton)
app.mount('#app');

