<template>
  <div>
    <Card>
      <div class="alarm-search-con search-con-top">
        <Select v-model="alarmSearchKey" class="search-col">
          <Option v-for="item in alarmFilterColumns" :value="item.key" :key="item.key">{{ item.title }}</Option>
        </Select>
        <Input clearable placeholder="输入关键字搜索" class="search-input" v-model="alarmSearchValue"/>
        <Button @click="handlerAlarmSearch" class="search-btn" type="primary">
          <Icon type="search"/>搜索
        </Button>
        <Button type="primary" @click="handlerBatchDeleteAlarm" class="handlerRemove">手动批量解除报警</Button>
      </div>
      <Table border ref="selection" search-place="top" :data="alarmTableData" :columns="alarmColumns"
             @on-sort-change="handlerAlarmSort"/>
      <Page :total="alarmPageTotal" :current="alarmPageNum" :page-size="alarmPageSize" show-sizer show-total
            @on-change="handlerAlarmPage"
            @on-page-size-change="handlerAlarmPageSize"/>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import './index.less'
import { alarmListApi, alarmBatchDeleteApi } from '@/api/alarm'

export default {
  name: 'tables_page',
  components: {
    Tables
  },
  data () {
    return {
      alarmSearchKey: '',
      alarmSearchValue: '',
      alarmPageTotal: 0,
      alarmPageNum: 1,
      alarmPageSize: 10,
      alarmOrderBy: 'alarm_refresh_time',
      alarmOrderType: 1,
      alarmFilterColumns: [
        { title: '报警名称', key: 'alarm_name' },
        { title: '报警详细信息', key: 'alarm_details' },
        { title: '报警级别', key: 'alarm_level' }
      ],
      alarmColumns: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        { title: '报警名称', key: 'alarm_name' },
        { title: '报警详细信息', key: 'alarm_details' },
        { title: '报警模块', key: 'alarm_module' },
        { title: '报警级别', key: 'alarm_level' },
        { title: '是否恢复', key: 'is_recover' },
        { title: '报警发生时间', key: 'alarm_happen_time', sortable: 'custom' },
        { title: '报警恢复时间', key: 'alarm_recover_time', sortable: 'custom' },
        { title: '报警刷新时间', key: 'alarm_refresh_time', sortable: 'custom', sortType: 'desc' }
      ],
      alarmTableData: []
    }
  },
  mounted () {
    this.queryAlarmList()
  },
  methods: {
    handlerAlarmSearch () {
      this.queryAlarmList()
    },
    handlerAlarmPage (value) {
      this.alarmPageNum = value
      this.queryAlarmList()
    },
    handlerAlarmPageSize (value) {
      this.alarmPageSize = value
      this.queryAlarmList()
    },
    handlerAlarmSort (column) {
      this.alarmOrderBy = column.key
      this.alarmOrderType = column.order === 'asc' ? 0 : 1
      this.queryAlarmList()
    },
    queryAlarmList () {
      alarmListApi(this.alarmPageNum, this.alarmPageSize, this.alarmOrderBy, this.alarmOrderType, this.alarmSearchKey, this.alarmSearchValue).then(res => {
        if (res.data.code !== 0) {
          this.$Message.info(res.data.description)
        } else {
          this.alarmTableData = res.data.data.data
          this.alarmPageTotal = res.data.data.total
          this.alarmPageNum = res.data.data.page
          this.alarmPageSize = res.data.data.size
        }
      })
    },
    handlerBatchDeleteAlarm () {
      let selectAlarmArray = this.$refs.selection.getSelection()
      let selectAlarmList = []
      for (let i = 0; i < selectAlarmArray.length; i++) {
        selectAlarmList.push(selectAlarmArray[i].alarm_md5)
      }
      if (selectAlarmList.length === 0) {
        this.$Message.info('请至少选择一个报警。')
      } else {
        alarmBatchDeleteApi(selectAlarmList).then(res => {
          this.$Message.info(res.data.description)
          this.queryAlarmList()
        })
      }
    }
  }
}
</script>
<style>
.ivu-page {
  margin-top: 30px;
  text-align: center;
}

.handlerRemove {
  float: right
}
</style>
