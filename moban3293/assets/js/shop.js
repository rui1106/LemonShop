var vm = new Vue({
    el: '#shop',
    // delimiters:["[[","]]"],
    data () {
        return {
          host,
          username:'',
          shopLists:[],
          shopdetail:'',
          category_id:''
        }
      },
    mounted(){
        let user = localStorage.username;    
        
        this.username = user;
        this.get_shop_data();
        this.get_category_id();
        this.get_show_goods();
      },
    methods:{
    fnQuit:function(){
       sessionStorage.clear();
       localStorage.clear();
       location.href = 'login.html';
    },
    get_shop_data:function(){
            var url = this.host + '/shop/';
            axios.get(url, {
                responseType: 'json',
            })
              .then(response => {
                    this.shopLists = response.data;
                   
                })
                .catch(error => {
                    console.log(error.response);
                })
    },
    goods_detail:function(id){
          location.href = 'single-product.html?sku_id='+id;
          // this.$router.push({path:'/single-product.html',query:{sku_id:id}});

    },
    get_show_goods:function(){
      // this.id = this.$route.query.sku_id;
          var url = this.host + '/shop_list/' + this.category_id + '/'
          axios.get(url, {
                responseType: 'json',
            })
              .then(response => {
                    this.shopLists = response.data;
                
                })
                .catch(error => {
                    console.log(error.response);
                })
       },
       // 从路径中提取sku_id  single-product.html?sku_id=1
        get_category_id: function(){
          // console.log("document.location.pathname="+document.location.toString())
            var re = /\/shop-list.html\?category_id=(\d)$/;
            this.category_id = document.location.toString().match(re)[1];
            if(!this.category_id){
              this.category_id = null;
            }
        },
  }
});