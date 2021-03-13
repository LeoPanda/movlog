/**
 * vueルーター定義
 */
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      //トップ画面
      path: '/',
      component: () => import('@/dashboard/Frame'),
      children: [
        {
          //ダッシュボード
          name: 'Dashboard',
          path: '/',
          component: () => import('@/dashboard/Dashboard'),
        },
        {
          //カード型映画一覧
          name: 'Movie List(Cards)',
          path: 'views/cards/',
          component: () => import('@/views/Cards'),
        },
        {
          //リスト型映画一覧
          name: 'Movie List(Table)',
          path: 'views/list/',
          component: () => import('@/views/EventList'),
        },
        {
          //映画詳細画面
          name: 'Detail',
          path: 'pages/card/:id',
          component: () => import('@/components/MovieDetail'),
          props: true
        },
        {
          //映画新規入力
          name: 'Add Movie',
          path: 'pages/card/new',
          component: () => import('@/components/MovieDetail'),
        },
        {
          //テーブルメンテナンス
          name: 'Table Maintanance',
          path: '/maintenance/tables',
          component: () => import('@/dashboard/components/TableMaint'),
        },
        {
          //Googleカレンダーからのデータリンク
          name: 'Link Google Calendar',
          path: '/maintenance/calendar',
          component: () => import('@/dashboard/components/LinkCalendar'),
        },
        {
          //データリロード
          name: 'reload data',
          path: '/maintenance/reload',
          component: () => import('@/dashboard/components/reload'),
        },
      ],
    },
  ],
})
