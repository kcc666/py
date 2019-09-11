var vm = new Vue({
    el: '#index',
    data: {

        allSH: {
            searchSH: true,
            verifySH: false,
            activeSH: false,
        },



        searchList: [],
        searchListName: [
            'LJ46792',
            'LJ97332',
            'LJ117388',
            'LJ119284',
            'LJ153286',
            'LJ194262',
            'LJ213751',
            'LJ231088',
            'LJ241792',
            'LJ242171',
            'LJ264545',
            'LJ304267',
            'LJ392981',
            'LJ492477',
            'LJ626978',
            'LJ836492',
            'LJ853875',
            'LJ905173',
        ],

        activeList: [],
        activeListName: [
            'LJ26863',
            'LJ78659',
            'LJ105576',
            'LJ122066',
            'LJ123831',
            'LJ143021',
            'LJ411569',
            'LJ449157',
        ],

        verifyList: [],
        verifyListName: [
            'LJ410340',
            'LJ652277',
            'LJ692712',
            'LJ877372',
            'LJ888365',
            'LJ926635',
        ],


    },
    methods: {
        restart: function (name) {

            var SearchList = $('table:eq(2) tr:gt(0)').length
            var a = []
            var b = ['LJ26863', 'LJ78659', 'LJ105576', 'LJ122066', 'LJ123831', 'LJ143021', 'LJ411569', 'LJ449157', 'LJ836492', 'LJ853875', 'LJ905173']
            for (var i = 0; i < SearchList; i++) {
                var itemStr = $('table:eq(2) tr:gt(0)').eq(i)[0].children[0].innerHTML
                a.push(itemStr)
            }
            //-------拿到AB数组
            for (let i = 0; i < b.length; i++) {
                if (a.indexOf(b[i]) == -1) {
                    console.log(b[i])
                }
            }



        },

        getVpsInfo: function () {
            var _this = this
            $.ajax({
                // async:false,
                type: "get",
                url: 'http://106.15.53.80:9001/all.txt',
                jsonpCallback: 'success',
                dataType: 'jsonp',
                success: function (data) {
                    console.log(data)

                    data.forEach(element => {

                        //判断把属于search的信息放进对应的列表
                        if (_this.searchListName.indexOf(element.computername) != -1) {
                            _this.searchList.push(element)
                        }

                        if (_this.activeListName.indexOf(element.computername) != -1) {
                            _this.activeList.push(element)
                        }

                        if (_this.verifyListName.indexOf(element.computername) != -1) {
                            _this.verifyList.push(element)
                        }




                    });

                    //拿到数据后再渲染进度条
                    layui.use('element', function () {
                        var element = layui.element;
                    })

                },
                error: function (e) {
                    console.log(e)
                }
            })
        },

        topSwitch: function (name) {
            switch (name) {
                case 'search':
                    this.allSH.searchSH = true;
                    this.allSH.verifySH = false;
                    this.allSH.activeSH = false;
                    break

                case 'verify':
                    this.allSH.searchSH = false;
                    this.allSH.verifySH = true;
                    this.allSH.activeSH = false;
                    break

                case 'active':
                    this.allSH.searchSH = false;
                    this.allSH.verifySH = false;
                    this.allSH.activeSH = true;
                    break
            }
        },

    },
    created: function () {

        this.getVpsInfo()


    }

})

