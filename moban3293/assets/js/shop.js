var vm = new Vue({
    el: '#shop',
    // delimiters:["[[","]]"],
    data () {
        return {
          host,
          username:'',
          shopLists:[],
          shopdetailList:[]
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
                    // alert(response.data.length);
                    this.shopLists = response.data;
                    // alert(this.categorysList[0].name);
                    // console.log(this.categorysList);
                    // for(let i=0;i<response.data.length;i++){
                    //     categorysList.push(response.data[i]);
                    //     alert(categorysList);
                    
                    
                // }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
      get_shop_detail:function(id){
        var url = this.host + '/single-product.html?id=' + id
        axios.get(url, {
                responseType: 'json',
            })
              .then(response => {
                    this.shopdetailList = response.data
                })
                .catch(error => {
                    console.log(error.response);
                })
      },

  }
});