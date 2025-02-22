<template>
  <div v-show="showBox" :class="mode == 'pop' ? 'mask' : ''">
    <div
      :class="mode == 'pop' ? 'verifybox' : ''"
      :style="{ 'max-width': parseInt(imgSize.width) + 30 + 'px' }"
    >
      <div v-if="mode == 'pop'" class="verifybox-top">
        请拖动滑块完成人机校验
        <span class="verifybox-close" @click="closeBox">
          <i class="iconfont icon-close"></i>
        </span>
      </div>
      <div
        class="verifybox-bottom"
        :style="{ padding: mode == 'pop' ? '15px' : '0' }"
      >
        <!-- 验证码容器 -->
        <component
          :is="componentType"
          v-if="componentType"
          ref="instance"
          :captcha-type="captchaType"
          :type="verifyType"
          :figure="figure"
          :arith="arith"
          :mode="mode"
          :v-space="vSpace"
          :explain="explain"
          :img-size="imgSize"
          :block-size="blockSize"
          :bar-size="barSize"
        ></component>
      </div>
    </div>
  </div>
</template>
<script type="text/babel">
/**
 * Verify 验证码组件
 * @description 分发验证码使用
 * */
import VerifySlide from './Verify/VerifySlide.vue'
import { useI18n } from '@/config'

export default {
  name: 'Vue2Verify',
  components: {
    VerifySlide
  },
  props: {
    captchaType: {
      type: String,
      required: true
    },
    figure: {
      type: Number
    },
    arith: {
      type: Number
    },
    mode: {
      type: String,
      default: 'pop'
    },
    vSpace: {
      type: Number
    },
    explain: {
      type: String
    },
    imgSize: {
      type: Object,
      default () {
        return {
          width: '310px',
          height: '155px'
        }
      }
    },
    blockSize: {
      type: Object
    },
    barSize: {
      type: Object
    }
  },
  data () {
    return {
      i18n: useI18n,
      clickShow: false,
      verifyType: undefined,
      componentType: ''
    }
  },
  computed: {
    showBox () {
      if (this.mode === 'pop') {
        return this.clickShow
      } else {
        return true
      }
    }
  },
  watch: {
    watchEffect () {
      switch (this.captchaType) {
        case 'blockPuzzle':
          this.verifyType = '2'
          this.componentType = 'VerifySlide'
          break
        case 'clickWord':
          this.verifyType = ''
          this.componentType = 'VerifyPoints'
          break
      }
    }
  },
  methods: {
    refresh () {
      if (this.$refs.instance.refresh) {
        this.$refs.instance.refresh()
      }
    },
    closeBox () {
      this.clickShow = false
      this.$refs.instance.refresh()
    },
    show () {
      if (this.mode === 'pop') {
        this.clickShow = true
      }
    }
  }
}
</script>

<style>
.verifybox {
  position: relative;
  box-sizing: border-box;
  border-radius: 2px;
  border: 1px solid #e4e7eb;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.verifybox-top {
  padding: 0 15px;
  height: 50px;
  line-height: 50px;
  text-align: left;
  font-size: 16px;
  color: #45494c;
  border-bottom: 1px solid #e4e7eb;
  box-sizing: border-box;
}

.verifybox-bottom {
  padding: 15px;
  box-sizing: border-box;
}

.verifybox-close {
  position: absolute;
  top: 13px;
  right: 9px;
  width: 24px;
  height: 24px;
  text-align: center;
  cursor: pointer;
}

.mask {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10001;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  /* display: none; */
  transition: all 0.5s;
  touch-action: none;
  touch-action: pan-y;
}

.verify-tips {
  position: absolute;
  left: 0px;
  bottom: 0px;
  width: 100%;
  height: 30px;
  line-height: 30px;
  color: #fff;
}

.suc-bg {
  background-color: rgba(92, 184, 92, 0.5);
  filter: progid:DXImageTransform.Microsoft.gradient(startcolorstr=#7f5CB85C, endcolorstr=#7f5CB85C);
}

.err-bg {
  background-color: rgba(217, 83, 79, 0.5);
  filter: progid:DXImageTransform.Microsoft.gradient(startcolorstr=#7fD9534F, endcolorstr=#7fD9534F);
}

.tips-enter,
.tips-leave-to {
  bottom: -30px;
}

.tips-enter-active,
.tips-leave-active {
  transition: bottom 0.5s;
}

/* ---------------------------- */
/*常规验证码*/
.verify-code {
  font-size: 20px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 5px;
  border: 1px solid #ddd;
}

.cerify-code-panel {
  height: 100%;
  overflow: hidden;
}

.verify-code-area {
  float: left;
}

.verify-input-area {
  float: left;
  width: 60%;
  padding-right: 10px;
}

.verify-change-area {
  line-height: 30px;
  float: left;
}

.varify-input-code {
  display: inline-block;
  width: 100%;
  height: 25px;
}

.verify-change-code {
  color: #337ab7;
  cursor: pointer;
}

.verify-btn {
  width: 200px;
  height: 30px;
  background-color: #337ab7;
  color: #ffffff;
  border: none;
  margin-top: 10px;
}

/*滑动验证码*/
.verify-bar-area {
  position: relative;
  background: #ffffff;
  text-align: center;
  -webkit-box-sizing: content-box;
  -moz-box-sizing: content-box;
  box-sizing: content-box;
  border: 1px solid #ddd;
  -webkit-border-radius: 4px;
}

.verify-bar-area .verify-move-block {
  position: absolute;
  top: 0px;
  left: 0;
  background: #fff;
  cursor: pointer;
  -webkit-box-sizing: content-box;
  -moz-box-sizing: content-box;
  box-sizing: content-box;
  box-shadow: 0 0 2px #888888;
  -webkit-border-radius: 1px;
}

.verify-bar-area .verify-move-block:hover {
  background-color: #337ab7;
  color: #ffffff;
}

.verify-bar-area .verify-left-bar {
  position: absolute;
  top: -1px;
  left: -1px;
  background: #f0fff0;
  cursor: pointer;
  -webkit-box-sizing: content-box;
  -moz-box-sizing: content-box;
  box-sizing: content-box;
  border: 1px solid #ddd;
}

.verify-img-panel {
  margin: 0;
  -webkit-box-sizing: content-box;
  -moz-box-sizing: content-box;
  box-sizing: content-box;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  border-radius: 3px;
  position: relative;
}

.verify-img-panel .verify-refresh {
  width: 25px;
  height: 25px;
  text-align: center;
  padding: 5px;
  cursor: pointer;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 2;
}

.verify-img-panel .icon-refresh {
  font-size: 20px;
  color: #fff;
}

.verify-img-panel .verify-gap {
  background-color: #fff;
  position: relative;
  z-index: 2;
  border: 1px solid #fff;
}

.verify-bar-area .verify-move-block .verify-sub-block {
  position: absolute;
  text-align: center;
  z-index: 3;
}

.verify-bar-area .verify-move-block .verify-icon {
  font-size: 18px;
}

.verify-bar-area .verify-msg {
  z-index: 3;
}

.iconfont {
  font-family: 'iconfont' !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-check:before {
  content: ' ';
  display: block;
  width: 32px;
  height: 32px;
  position: absolute;
  margin: auto;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 9999;
  background-image: url('../../assets/icons/icon-done.svg');
  background-size: contain;
}

.icon-close:before {
  content: ' ';
  display: block;
  width: 32px;
  height: 32px;
  position: absolute;
  margin: auto;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 9999;
  background-image: url('../../assets/icons/icon-cancel.svg');
  background-size: contain;
}

.icon-right:before {
  content: ' ';
  display: block;
  width: 32px;
  height: 32px;
  position: absolute;
  margin: auto;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-size: cover;
  z-index: 9999;
  background-image: url('../../assets/icons/icon-chevron-right.svg');
  background-size: contain;
}

.icon-refresh:before {
  content: ' ';
  display: block;
  width: 24px;
  height: 24px;
  position: absolute;
  margin: auto;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 9999;
  background-image: url('../../assets/icons/icon-refresh.svg');
  background-size: contain;
}
</style>
