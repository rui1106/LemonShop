var vm = new Vue({
    el: '#shop',
    // delimiters:["[[","]]"],
    data () {
        return {
          host,
          username:'',
          shopLists:[],
          shopdetail:'',
        }
      },
    mounted(){
        let user = localStorage.username;    
        
        this.username = user;
        this.get_shop_data();

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
     

  }
});