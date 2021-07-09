// var vm = new Vue({
//   el:'#index',
//   data:{
//      username:''
//   },
//   methods:{
//     let user = localStorage.username;    
//     if(user==undefined)
//     {
//       this.username = false;
//        // this.$router.push({path:'/'});
//        return;
//     }
//     this.username = user;
//   }
//   // methods:{
//   //   fnQuit:function(){
//   //      sessionStorage.clear();
//   //      localStorage.clear();
//   //      this.$router.push({path:'/'});
//   //   }
//   // }
// })
var vm = new Vue({
    el: '#index',
    // delimiters:["[[","]]"],
    data () {
        return {
          host,
          username:'',
          categorysList:[],
        }
      },
    mounted(){
        let user = localStorage.username;    
        
        this.username = user;
        this.get_category_data();

      },
    methods:{
    fnQuit:function(){
       sessionStorage.clear();
       localStorage.clear();
       location.href = 'login.html';
    },
    get_category_data:function(){
            var url = this.host + '/category/';
            axios.get(url, {
                responseType: 'json',
            })
              .then(response => {
                    // alert(response.data.length);
                    this.categorysList = response.data;
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
  }
});