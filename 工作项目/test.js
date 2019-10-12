

        /**
         * bookingTicket 초기화
         */
        $(document).ready(function(){
            var _t = 'ecfbb8ce-1e5a-4757-8cc2-daa116d6f248';
            $('input.bookingTicket').val(_t);
        });

        /**
         * 인원수 증감 기호 cursor:pointer 적용
         */
        $(document).ready(function(){
            $('span.btn_minus,span.btn_plus').css('cursor','pointer');
        });


        // 선택지 클릭시 이벤트
        $('.selected_area').on('click', function() {
            $(this).removeClass('on');
            $(this).parents('.input_wrap').find('input').focus();
        });

        //입력값이 있을때 표시
        $('.input_wrap input.booking').on('keydown keyup change', function(){
            var Length = $(this).val().length;
            if(Length > 0){
                $(this).parents('.input_wrap').addClass('on');
            }else{
                $(this).parents('.input_wrap').removeClass('on');
            }
        });

        //포커스 추가
        //$(".input_wrap .btn_minus, .input_wrap .btn_plus").attr("tabindex", 0);

        /**
         * 공항 검색 input box focus out 된 경우 아이콘 처리
         */
        var checkAirportPinStatus = function(inputObj, routeIndex){

            var tripType = $('input[name="tripType"]:checked').val();

            if($(inputObj).hasClass('start') && $('input[name="availabilitySearches['+routeIndex+'].depAirport"]').val()!=''){
                $(inputObj).parents('div.input_wrap').find('div.selected_area').addClass('on');
                $(inputObj).parents('div.input_wrap').addClass('focus');
            }
            else if($(inputObj).hasClass('end') && $('input[name="availabilitySearches['+routeIndex+'].arrAirport"]').val()!=''){
                $(inputObj).parents('div.input_wrap').find('div.selected_area').addClass('on');
                $(inputObj).parents('div.input_wrap').addClass('focus');
            }
            else{
                $(inputObj).parents('div.input_wrap').find('div.selected_area').removeClass('on');
                $(inputObj).parents('div.input_wrap').removeClass('focus');
            }

        };

        /**
         * 레이어 바깥부분 클릭한 경우 모든 레이어 숨김
         */
        $(document).ready(function(){
            $.fn.bookingCommonLayerClick();
        });

        /**
         * 한국지역 선택시에만 단체 선택 노출
         */
        $(document).ready(function(){
            /*
            // 한국지역이 아닌경우 단체 미노출, if('KR' != 'KR'){
            if('CN' != 'KR'){
                $('div.res_grouping').hide();
            }
            */
        });

        /**
         * trip type 선택 event handling
         */
        $(document).ready(function(){

            var frm = $('#airAvailabilityRQ');

            // $('div.sel_section.booking_option input[name="tripTypeButton"]').on('change', function(){
            //     var tripType = $('div.sel_section.booking_option input[name="tripTypeButton"]:checked').val();
            //
            //     alert(tripType);
            //
            //     $.each(frm.find('input[name="tripType"]'),function(index,el){
            //         if($(el).val()==tripType){
            //             $(el).prop('checked',true);
            //             checkTripType();
            //         }
            //     });
            //
            // });

            // 다구간 검색 진입 처리
            var paramTripType = '';
            $.each(frm.find('input[name="tripType"]'),function(index,el){
                if($(el).val()==paramTripType){
                    $(el).prop('checked',true);
                    checkTripType();
                    return false;
                }
            });

        });


        /**
         * 출발노선선택 레이어 준비
         */
        $(document).ready(function(){
            // gnbRouteDeparture($('input[name="tripType"]:checked').val());
        });

        /**
         * TripType 선택시 출발노선 레이어 준비
         */
        // $('input[name="tripType"]').change(function(){
        //     removeLayer('route_departure');
        //     gnbRouteDeparture($(this).val());
        // });

        /**
         * 탑승객 수 선택 event handling
         */
        $(document).ready(function(){

            // RQ
            var pax_count = {};
            pax_count = {'ADULT' : 0, 'CHILD' : 0, 'INFANT' : 0 };

            var _pax_list = [{'paxCount':1,'paxType':'ADULT'},{'paxCount':0,'paxType':'CHILD'},{'paxCount':0,'paxType':'INFANT'}];

            $.each(_pax_list, function(pi,pp){
                if($.trim(pp.paxType)!=''){
                    pax_count[pp.paxType] = pp.paxCount;
                }
            });

            $.each($('.pax input'), function(){
                if(parseInt(pax_count[$(this).data('div')],10) > 0){
                    $(this).val(pax_count[$(this).data('div')]);
                }
            });

            // 성인 탑승자수 변경 이벤트 처리
            $('.pax input').change(function(){
                choosePaxCount($(this));
            });

        });

        var changePaxCount = function(div, count){

            // console.log('#### changePaxCount : ' + div +'/'+count);
            var paxCount = parseInt($('.pax input.'+div).val(),10);


            if(count>0){
                $('.pax input.'+div).val(paxCount+1);
            }
            else if(div =='ADULT' && count<0 && paxCount>1){
                $('.pax input.'+div).val(paxCount-1);
            }
            else if(div !='ADULT' && count<0 && paxCount>0){
                $('.pax input.'+div).val(paxCount-1);
            }

            choosePaxCount($('.pax input.'+div));

        };


        /**
         * 상단 단체 체크박스 이벤트 처리
         */
        $(document).ready(function(){
            $('input.bookingTypeGroup').change(function(){

                /**
                 * 개인 -> 단체 예약 전환
                 * 성인 소아 유아 : 10 0 0 으로 설정 및 form 초기화
                 */
                if($(this).prop('checked')){

                	var deepLinkInfo = null;
                	var alert_msg_group_corporate = '\u516C\u53F8\u6298\u6263\u4E0D\u9002\u7528\u4E8E\u56E2\u4F53\u7968\u3002';	//단체항공권은 기업 우대 할인이 적용되지 않습니다.
                	
                	if(deepLinkInfo != null && deepLinkInfo.deepLinkDiv == 'C'){
                		alert(alert_msg_group_corporate);
                	}
                	
                	$('.pax input.ADULT').val(10);
                    $('.pax input.CHILD').val(0);
                    $('.pax input.INFANT').val(0);

                    initSearchForm();
                }
                /**
                 * 단체 -> 개인 예약 전환
                 * 성인 소아 유아 : 1 0 0 으로 설정, 구간, 일정 form은 초기화 하지 않습니다.
                 */
                else{
                    $('.pax input.ADULT').val(1);
                    $('.pax input.CHILD').val(0);
                    $('.pax input.INFANT').val(0);

                    setBookingType();
                }
            });
        });

        /**
         * 인원선택 변경에 따른 bookingType 전환
         */
        var setBookingType = function(){

            var paxCount = parseInt($('.pax input.ADULT').val(),10) + parseInt($('.pax input.CHILD').val(),10);

            // console.log('setBookingType : ' + paxCount);

            $.each($('input[name="bookingType"]'), function(index,el){

                // 개인
                if($(el).val()=='HI' && paxCount<10){

                    $('input.bookingTypeGroup').prop('checked', false);

                    $(el).prop('checked', true);
                    // $('.controlRouteCountButtonSection').show(); // 다구간 구간 증/감 버튼 영역 노출

                    $('input[name="paxCountDetails[0].paxCount"]').val($('.pax input.ADULT').val());
                    $('input[name="paxCountDetails[1].paxCount"]').val($('.pax input.CHILD').val());
                    $('input[name="paxCountDetails[2].paxCount"]').val($('.pax input.INFANT').val());
                }
                // 단체
                else if($(el).val()=='HG' && paxCount>=10){
                    $(el).prop('checked', true);
                    // $('.controlRouteCountButtonSection').hide(); // 다구간 구간 증/감 버튼 영역 비노출
                }
            });

            pax_count_before_change[0] = parseInt($('input[name="paxCountDetails[0].paxCount"]').val(),10);
            pax_count_before_change[1] = parseInt($('input[name="paxCountDetails[1].paxCount"]').val(),10);
            pax_count_before_change[2] = parseInt($('input[name="paxCountDetails[2].paxCount"]').val(),10);
        };

        var pax_count_individual = 9; // 개인 최대 인원 수
        var pax_count_group = 30; // 단체 최대 인원 수
        var pax_count_before_change = [1,0,0]; // 인원수 변경 이전 최종 여행객 수
        var alert_msg_max_pax = '\u6210\u4EBA\u4E0E\u513F\u7AE5\u4EBA\u5458\u4E00\u8D77\u6700\u591A\u53EF\u900930\u4EBA\u3002';//'성인과 소아 인원을 합해 30명까지 선택 가능합니다.';
        var alert_msg_max_infant_pax = '\u4E00\u540D\u5A74\u513F\u5FC5\u987B\u7531\u4E00\u540D\u6210\u4EBA\u966A\u4F34\u3002';//'유아 1명당 성인 1명이 반드시 동반되어야 합니다.';
        var alert_msg_chage_group_booking = '\u4E3A\u4E86\u68C0\u7D22\u56E2\u4F53\u673A\u7968\uFF0C\u8981\u521D\u59CB\u5316\u5DF2\u9009\u62E9\u7684\u4FE1\u606F\u5417\uFF1F';//'단체 항공권 검색을 위해 선택한 정보를 초기화 하시겠습니까?';
        var alert_msg_chage_individual_booking = '\u4E3A\u4E86\u673A\u7968\u518D\u68C0\u7D22\uFF0C\u8981\u521D\u59CB\u5316\u5DF2\u9009\u62E9\u7684\u4FE1\u606F\u5417\uFF1F';// '항공권 재 검색을 위해 선택한 정보를 초기화 하시겠습니까?';

        $(document).ready(function(){
            pax_count_before_change[0] = parseInt($('input[name="paxCountDetails[0].paxCount"]').val(),10);
            pax_count_before_change[1] = parseInt($('input[name="paxCountDetails[1].paxCount"]').val(),10);
            pax_count_before_change[2] = parseInt($('input[name="paxCountDetails[2].paxCount"]').val(),10);
        });

        var choosePaxCount = function(el){


            // 구분별 탑승자수
            var pax_count = [];
            pax_count.push(parseInt($('.pax input.ADULT').val(),10)); // 성인
            pax_count.push(parseInt($('.pax input.CHILD').val(),10)); // 소아
            pax_count.push(parseInt($('.pax input.INFANT').val(),10)); // 유아

            // console.log('여행객 수 변경 '+(pax_count_before_change[0]+pax_count_before_change[1])+'->'+(pax_count[0]+pax_count[1]))

            // console.log(pax_count[0]+'/'+pax_count[1]+'/'+pax_count[2]);

            // 개인 -> 단체 전환
            if((pax_count_before_change[0]+pax_count_before_change[1])<=pax_count_individual && pax_count[0] + pax_count[1] > pax_count_individual){
                // console.log('개인 -> 단체 전환');

                // 개인 -> 단체 전환
                if(confirm(alert_msg_chage_group_booking)){

                    // 단체 checkbox check !!
                    $('input[name="bookingTypeGroup"]').prop('checked', true);

                    // 최종 변경된 여행객 수 저장
                    pax_count_before_change[0] = pax_count[0];
                    pax_count_before_change[1] = pax_count[1];
                    pax_count_before_change[2] = pax_count[2];

                    initSearchForm();

                }
                else{

                    // 단체 checkbox check 해제 !!
                    $('input[name="bookingTypeGroup"]').prop('checked', false);

                    // 이전 선택 여행객수로 되돌려줍니다.
                    $('.pax input.ADULT').val(pax_count_before_change[0]);
                    $('.pax input.CHILD').val(pax_count_before_change[1]);
                    $('.pax input.INFANT').val(pax_count_before_change[2]);

                    $('input[name="paxCountDetails[0].paxCount"]').val(pax_count_before_change[0]);
                    $('input[name="paxCountDetails[1].paxCount"]').val(pax_count_before_change[1]);
                    $('input[name="paxCountDetails[2].paxCount"]').val(pax_count_before_change[2]);

                    return false;
                }


            }
            // 단체 -> 개인 전환
            else if((pax_count_before_change[0]+pax_count_before_change[1])>pax_count_individual && pax_count[0] + pax_count[1] <= pax_count_individual){
                // console.log('단체 -> 개인 전환');


                /**
                 * 단체 -> 개인 전환시 form 초기화 하지 않기로 정책 변경. 2019-01-11
                 */

                /*

                // 단체 -> 개인 전환
                if(confirm(alert_msg_chage_individual_booking)){

                    // 단체 checkbox check !!
                    $('input[name="bookingType"]').prop('checked', false);

                    // 최종 변경된 여행객 수 저장
                    pax_count_before_change[0] = pax_count[0];
                    pax_count_before_change[1] = pax_count[1];
                    pax_count_before_change[2] = pax_count[2];

                    initSearchForm();

                }
                else{

                    // 단체 checkbox check 해제 !!
                    $('input[name="bookingType"]').prop('checked', true);

                    // 이전 선택 여행객수로 되돌려줍니다.
                    $('.pax select.ADULT').val(pax_count_before_change[0]);
                    $('.pax select.CHILD').val(pax_count_before_change[1]);
                    $('.pax select.INFANT').val(pax_count_before_change[2]);

                    return false;
                }
                */
                setBookingType();

            }

            // 30인 이상 초과
            if(pax_count[0] + pax_count[1] > pax_count_group){

                alert(alert_msg_max_pax);

                // 이전 선택 여행객수로 되돌려줍니다.
                $('.pax input.ADULT').val(pax_count_before_change[0]);
                $('.pax input.CHILD').val(pax_count_before_change[1]);
                $('.pax input.INFANT').val(pax_count_before_change[2]);

                return false;
            }

            // 성인 탑승자수 변경 이벤트 처리
            if($(el).attr('class') == 'ADULT'){
            };

            // 소아 탑승자수 변경 이벤트 처리
            if($(el).attr('class') == 'CHILD'){

            };

            // 유아 탑승자수 변경 이벤트 처리
            // if($(el).hasClass('INFANT')){
                // 성인 숫자보다 많은 경우
                if(pax_count[0] < pax_count[2]){
                    alert(alert_msg_max_infant_pax);
                    pax_count[2] = pax_count[0];
                    $('.pax input.INFANT').val(pax_count[2]);
                    pax_count_before_change[2] = pax_count[2];
                }
            // };

            $('input[name="paxCountDetails[0].paxCount"]').val(pax_count[0]);
            $('input[name="paxCountDetails[1].paxCount"]').val(pax_count[1]);
            $('input[name="paxCountDetails[2].paxCount"]').val(pax_count[2]);

        };

        /**
         * 입력폼 초기화
         */
        var initSearchForm = function(){

            /**
             * airAvailabilityRQ form reset
             */
            $('#airAvailabilityRQ input.reset_target').val('');

            /**
             * display 영역 초기화
             */
            // tripType = RT
            // $('div.tab_section ul.chk_rdo_list input[name="tripTypeButton"]').eq(0).prop('checked', true);
            // $('div.tab_section ul.chk_rdo_list input[name="tripTypeButton"]').trigger('change');
            checkTripType();

            // 왕복/편도 공항, 출도착일 정보
            var alert_msg_city_airport = '\u57CE\u5E02/\u673A\u573A';

            $('#main_reser01 div.start').removeClass('focus');
            $('#main_reser01 div.start div.selected_area').removeClass('on');

            $('#main_reser01 div.end').removeClass('focus');
            $('#main_reser01 div.end div.selected_area').removeClass('on');

            $('#main_reser01 div.date').removeClass('focus');
            $('#main_reser01 div.date input').val('');


            $('#main_reser02 div.start').removeClass('focus');
            $('#main_reser02 div.start div.selected_area').removeClass('on');

            $('#main_reser02 div.end').removeClass('focus');
            $('#main_reser02 div.end div.selected_area').removeClass('on');

            $('#main_reser02 div.date').removeClass('focus');
            $('#main_reser02 div.date input').val('');

            // 다구간 공항, 출도착일 정보
            multiTripItineraryCount = 2;
            for(var i=0 ; i<4 ; i++){

                $('#itinerary_multi_trip_'+(i+1)+' div.start').removeClass('focus');
                $('#itinerary_multi_trip_'+(i+1)+' div.start div.selected_area').removeClass('on');

                $('#itinerary_multi_trip_'+(i+1)+' div.end').removeClass('focus');
                $('#itinerary_multi_trip_'+(i+1)+' div.end div.selected_area').removeClass('on');

                $('#itinerary_multi_trip_'+(i+1)+' div.date').removeClass('focus');
                $('#itinerary_multi_trip_'+(i+1)+' div.date input').val('');


                if(i<2){
                    $('#itinerary_multi_trip_'+(i+1)).show();
                }
                else{
                    $('#itinerary_multi_trip_'+(i+1)).hide();
                }

            }

            $('input[name="paxCountDetails[0].paxCount"]').val($('.pax input.ADULT').val());
            $('input[name="paxCountDetails[1].paxCount"]').val($('.pax input.CHILD').val());
            $('input[name="paxCountDetails[2].paxCount"]').val($('.pax input.INFANT').val());

            setBookingType();

        };

        /**
         * tripType 선택에 따른 form control
         */
        $(document).ready(function(){

            // set event handler
            $('input[name="tripType"]').change(function(){
                checkTripType();
            });

            checkTripType();
        });

        var checkTripType = function(){
            var tripType = $('input[name="tripType"]:checked').val();
            $('ul.sel_section li').removeClass('on');

            // 왕복
            if(tripType == 'RT'){
                $('#main_reser01').show();
                $('#main_reser02').hide();
                $('#main_reser03').hide();

                $('ul.sel_section li').eq(0).addClass('on');
                $('.sel_section li a').removeAttr('title');
                $('.sel_section li.on a').attr('title','선택됨');



                // 편도 출발정보가 있는 경우 돌아오는편 정보에 설정
                if($('input[name="availabilitySearches[0].depAirport"]').val()!='' && $('input[name="availabilitySearches[0].arrAirport"]').val()!=''){
                    $('input[name="availabilitySearches[1].depAirport"]').val($('input[name="availabilitySearches[0].arrAirport"]').val());
                    $('input[name="availabilitySearches[1].arrAirport"]').val($('input[name="availabilitySearches[0].depAirport"]').val());
                }

            }
            // 편도
            else if(tripType == 'OW') {
                $('#main_reser01').hide();
                $('#main_reser02').show();
                $('#main_reser03').hide();
                $('ul.sel_section li').eq(1).addClass('on');
                $('.sel_section li a').removeAttr('title');
                $('.sel_section li.on a').attr('title','선택됨');


                // 날짜 표출 영역, 출발일만 노출
                // console.log($('#main_reser01 .multiple .wave').length);
                // console.log($('#main_reser01 .multiple .wave').html());

            }
            // 다구간
            else if(tripType == 'MC') {
                $('#main_reser01').hide();
                $('#main_reser02').hide();
                $('#main_reser03').show();

                $('ul.sel_section li').eq(2).addClass('on');
                $('.sel_section li a').removeAttr('title');
                $('.sel_section li.on a').attr('title','선택됨');
            }
        };


        /**
         * 다구간 여정 관리
         */
        var currentItineraryNumber = 1; // 현재 선택 진행중인 여정 구간
        var minMultiTripItineraryCount = 2; // 최소 여정 수
        var maxMultiTripItineraryCount = 4; // 최대 여정 수
        var multiTripItineraryCount = 2; // 초기 여정 수

        /**
         * 여정삭제
         */
        var decreaseItinerary = function(){

            if(multiTripItineraryCount == minMultiTripItineraryCount){
                return false;
            }
            else{
                $('#itinerary_multi_trip_' + (multiTripItineraryCount)).find('input[type="text"]').val('');
                $('#itinerary_multi_trip_' + (multiTripItineraryCount)).hide();


                var init_airport_name = '\u57CE\u5E02/\u673A\u573A';  // 도시/공항

                $('#itinerary_multi_trip_' + multiTripItineraryCount).find('.departure').addClass('inacctive');
                $('#itinerary_multi_trip_' + multiTripItineraryCount).find('.arrival').addClass('inacctive');
                $('#itinerary_multi_trip_' + multiTripItineraryCount).find('.schedule').addClass('inacctive');

                $('#itinerary_multi_trip_' + multiTripItineraryCount).find('.departure .airport_name').text(init_airport_name);
                $('#itinerary_multi_trip_' + multiTripItineraryCount).find('.arrival .airport_name').text(init_airport_name);

                multiTripItineraryCount--;
            }

        };


        /**
         * 여정추가
         */
        var increaseItinerary = function(){
            if(multiTripItineraryCount == maxMultiTripItineraryCount){
                return false;
            }
            else{
                multiTripItineraryCount++;
                $('#itinerary_multi_trip_' + (multiTripItineraryCount)).show();
            }
        };


        /**
         * 여정선택완료, 다음으로 이동
         */
        var chooseItinerary = function(){

            var alert_msg_choose_itinerary = '\u8BF7\u9009\u62E9\u8981\u65C5\u884C\u7684\u822A\u7EBF\u3002'; //여행하실 노선을 선택해주세요.
            var alert_msg_choose_schedule = '\u8BF7\u9009\u62E9\u51FA\u53D1\u65E5\u3002'; // 출발일을 선택해주세요.
            var alert_msg_choose_schedule_roundtrip = '\u8BF7\u90FD\u9009\u62E9\u51FA\u53D1\u65E5\u548C\u5230\u8FBE\u65E5\u3002'; // 출/도착일을 모두 선택해주세요.
            var alert_msg_check_promocode = '\u8BF7\u786E\u8BA4\u5DF2\u8F93\u5165\u4FC3\u9500\u4EE3\u7801\u7684\u6253\u6298\u89C4\u5B9A\u3002'; // '입력하신 프로모션코드의 할인규정을 확인해주세요.';
            var alert_msg_connect_flight_surface = '\u7B2C{0}\u533A\u95F4\u7684\u5230\u8FBE\u673A\u573A\u4E0E\u7B2C{1}\u533A\u95F4\u7684\u51FA\u53D1\u673A\u573A\u5E94\u5728\u540C\u4E00\u5730\u533A\uFF08\u5927\u9646\uFF09\u3002'; // '{0}번째 구간의 도착공항과 {1}번째 구간 출발공항은 같은 지역(대륙)이어야 합니다.';
            var alert_msg_connect_flight_surface_reverse = '\u7B2C{0}\u6BB5\u51FA\u53D1\u673A\u573A\u548C\u7B2C{1}\u6BB5\u5230\u8FBE\u673A\u573A\u5FC5\u987B\u4E3A\u540C\u4E00\u5730\u533A(\u5927\u9646)\u3002'; // '{0}번째 구간의 출발공항과 {1}번째 구간 도착공항은 같은 지역(대륙)이어야 합니다.';

            var alert_msg_max_length_stay = '\u7B2C\u4E00\u533A\u95F4\u7684\u51FA\u53D1\u65E5\u81F3\u6700\u540E\u533A\u95F4\u7684\u5230\u8FBE\u65E5\u5176\u65F6\u95F4\u4E0D\u5F97\u8D85\u8FC7365\u5929\u3002'; // '첫번째 구간의 출발일에서 마지막 구간의 도착일까지의 기간은 365일을 초과할 수 없습니다.';
            var alert_msg_connect_schedule = '\u533A\u95F4{0}\u7684\u51FA\u53D1\u65E5\u4E0D\u80FD\u9009\u62E9\u5FEB\u4E8E\u533A\u95F4{1}\u7684\u51FA\u53D1\u65E5\u3002'; // '구간{0}의 출발일은 구간{1}의 출발일보다 빠른날짜를 선택할 수 없습니다.';
            var alert_msg_connect_combination = '\u806F\u7A0B\u4E0D\u80FD\u8207\u570B\u969B\u7DDA\u548C\u570B\u5167\u7DDA\u4E00\u540C\u9810\u7D04\u3002';// '다구간 여정은 국제선, 국내선 노선을 함께 예약할 수 없습니다.'

            var frm = $('#airAvailabilityRQ');

            frm.find('input.rqParam').remove();

            // 탑승객
            frm.append('<input type="hidden" name="pax" class="rqParam" value="'+ $('input[name="paxCountDetails[0].paxCount"]').val() +'"/>');
            frm.append('<input type="hidden" name="pax" class="rqParam" value="'+ $('input[name="paxCountDetails[1].paxCount"]').val() +'"/>');
            frm.append('<input type="hidden" name="pax" class="rqParam" value="'+ $('input[name="paxCountDetails[2].paxCount"]').val() +'"/>');

            // promoCode 입력된 경우 규정 확인 및 유효성 통과 여부 체크 - 개인만 적용, 유효성 체크하지 않는 것으로 변경합니다.
            // 기업우대 예약인 경우 promoCode 세팅
            var promoCode = "";
            var deepLinkInfo = null;
            if(deepLinkInfo != null){
            	promoCode = deepLinkInfo.promoCode;
            } else if($('div.code input[name="promoCode"]').val().length>0){
            	promoCode = $('div.code input[name="promoCode"]').val();
            }
            
            if($('input[name="bookingType"]:checked').parent().attr('id') == 'bookingType_individual'){

                if(promoCode.length>0){
                    var isValid = false;
                    $.ajax({
                        url : '/ajax/layerComponents/discountCodeRule', // ajax url
                        dataType : 'json', // ajax 통신의 데이터 형식
                        async : false,  // 동기(false):비동기(true)
                        type : 'get',
                        data : {
                            promoCode:promoCode
                        },
                        success : function(data){
                            // console.log(data);
                            if(data.success){
                            	frm.append('<input type="hidden" name="promoCode" class="rqParam" value="'+ promoCode +'"/>');
                                isValid = true;
                            } else {
                                alert(alert_msg_check_promocode);
                            }
                        }
                    });
                    
                    if(!isValid) {
                        return false;
                    }
                }
            }

            //왕복
            if($('#tripType_RT:checked').length==1) {

                // 노선 선택 여부
                if($('input[name="availabilitySearches[0].depAirport"]').val()=='' || $('input[name="availabilitySearches[1].depAirport"]').val()==''
                    || $('input[name="availabilitySearches[0].arrAirport"]').val()=='' || $('input[name="availabilitySearches[1].arrAirport"]').val()==''){
                    alert(alert_msg_choose_itinerary);
                    return false;
                }

                // 출/도착일 선택 여부
                if($('input[name="availabilitySearches[0].flightDate"]').val()=='' || $('input[name="availabilitySearches[1].flightDate"]').val()==''){
                    alert(alert_msg_choose_schedule_roundtrip);
                    return false;
                }

                // 출발공항정보
                frm.append('<input type="hidden" name="deptAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[0].depAirport"]').val() +'"/>');
                frm.append('<input type="hidden" name="deptAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[1].depAirport"]').val() +'"/>');

                // 도착공항정보
                frm.append('<input type="hidden" name="arriAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[0].arrAirport"]').val() +'"/>');
                frm.append('<input type="hidden" name="arriAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[1].arrAirport"]').val() +'"/>');

                // 출발일 정보
                frm.append('<input type="hidden" name="schedule" class="rqParam" value="'+ $('input[name="availabilitySearches[0].flightDate"]').val() +'"/>');
                frm.append('<input type="hidden" name="schedule" class="rqParam" value="'+ $('input[name="availabilitySearches[1].flightDate"]').val() +'"/>');

            }
            // 편도
            else if($('#tripType_OW:checked').length==1) {

                // 노선 선택 여부
                if($('input[name="availabilitySearches[0].depAirport"]').val()=='' || $('input[name="availabilitySearches[0].arrAirport"]').val()==''){
                    alert(alert_msg_choose_itinerary);
                    return false;
                }

                // 출발일 선택 여부
                if($('input[name="availabilitySearches[0].flightDate"]').val()==''){
                    alert(alert_msg_choose_schedule);
                    return false;
                }

                // 출발공항정보
                frm.append('<input type="hidden" name="deptAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[0].depAirport"]').val() +'"/>');

                // 도착공항정보
                frm.append('<input type="hidden" name="arriAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches[0].arrAirport"]').val() +'"/>');

                // 출발일 정보
                frm.append('<input type="hidden" name="schedule" class="rqParam" value="'+ $('input[name="availabilitySearches[0].flightDate"]').val() +'"/>');

            }
            // 다구간인경우
            else if($('#tripType_MC:checked').length==1){

                for(var i=0 ; i<multiTripItineraryCount ; i++){
                    // 노선 선택 여부
                    if($('input[name="availabilitySearches['+i+'].depAirport"]').val()=='' || $('input[name="availabilitySearches['+i+'].arrAirport"]').val()==''){
                        alert(alert_msg_choose_itinerary);
                        return false;
                    }
                    // 출발일 선택 여부
                    if($('input[name="availabilitySearches['+i+'].flightDate"]').val()==''){
                        alert(alert_msg_choose_schedule);
                        return false;
                    }
                }


                for(var i=0 ; i<multiTripItineraryCount ; i++){
                    // 출발공항정보
                    frm.append('<input type="hidden" name="deptAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches['+i+'].depAirport"]').val() +'"/>');
                    // 도착공항정보
                    frm.append('<input type="hidden" name="arriAirportCode" class="rqParam" value="'+ $('input[name="availabilitySearches['+i+'].arrAirport"]').val() +'"/>');
                    // 출발일 정보
                    frm.append('<input type="hidden" name="schedule" class="rqParam" value="'+ $('input[name="availabilitySearches['+i+'].flightDate"]').val() +'"/>');
                }


                /**
                 * 연결구간 surface 점검, 출발일 점검
                 */
                for(var i=1 ; i<multiTripItineraryCount ; i++) {

                var beforeAirport = $('input[name="availabilitySearches['+(i-1)+'].arrAirport"]');
                    var afterAirport = $('input[name="availabilitySearches['+i+'].depAirport"]');

                    if( beforeAirport.data('conti') != afterAirport.data('conti') ){
                        alert(alert_msg_connect_flight_surface.replace('{0}', i).replace('{1}', (i+1)));
                        return false;
                    }

                    //-- #368 [공통] 다국간 정책 변경 건 추가
                    beforeAirport = $('input[name="availabilitySearches['+(i-1)+'].depAirport"]');
                    afterAirport = $('input[name="availabilitySearches['+i+'].arrAirport"]');

                    if( beforeAirport.data('conti') != afterAirport.data('conti') ){
                        alert(alert_msg_connect_flight_surface_reverse.replace('{0}', i).replace('{1}', (i+1)));
                        return false;
                    }
                    //-- #368 [공통] 다국간 정책 변경 건 추가

                    var beforeDeparture = parseInt($('input[name="availabilitySearches['+(i-1)+'].flightDate"]').val().replace(/-/gi, ""),10);
                    var afterDeparture = parseInt($('input[name="availabilitySearches['+(i)+'].flightDate"]').val().replace(/-/gi, ""),10);

                    if(afterDeparture < beforeDeparture){
                        alert(alert_msg_connect_schedule.replace('{0}', (i+1)).replace('{1}', (i)));
                        return false;
                    }

                }


                /**
                 * 국제선, 국내선 결합 금지
                 */
                var domIntStatus = '';
                for(var i=0 ; i<multiTripItineraryCount ; i++) {
                    var beforeAirport = $('input[name="availabilitySearches[' + i + '].arrAirport"]');
                    var afterAirport = $('input[name="availabilitySearches[' + i + '].depAirport"]');

                    // 출발, 도착 중 한곳이라도 한국이 아니면 국제산
                    if( (beforeAirport.data('conti')!='SKR' || afterAirport.data('conti')!='SKR') && domIntStatus.indexOf('I')==-1){
                        domIntStatus += 'I';
                    }

                    // 출발, 도착 모두 한국인 경우 국내선
                    if( beforeAirport.data('conti')=='SKR' && afterAirport.data('conti')=='SKR' && domIntStatus.indexOf('D')==-1){
                        domIntStatus += 'D';
                    }
                }

                if(domIntStatus.length>1){
                    alert(alert_msg_connect_combination);
                    return false;
                }


                /**
                 * 최대체류기간 점검, max 365 day
                 */
                var date1 = $('input[name="availabilitySearches[0].flightDate"]').val().replace(/-/gi, "");
                var date2 = $('input[name="availabilitySearches['+(multiTripItineraryCount-1)+'].flightDate"]').val().replace(/-/gi, "");


                if(dateIntervalDay(date1, date2)>365){
                    alert(alert_msg_max_length_stay);
                    return false;
                };

            }


            /**
             * 단체항공권 관련 체크
             * 1. 로그인 여부
             * 2. 1일 최대 예약 건수 - 2회
             */
            var groupBookingFlag = parseInt($('input[name="paxCountDetails[0].paxCount"]').val(),10) + parseInt($('input[name="paxCountDetails[1].paxCount"]').val(),10) > 9;

            if(groupBookingFlag){

                var alert_msg_ruquest_login_grp_booking = '\u767B\u5F55\u540E\u65B9\u53EF\u4F7F\u7528\u56E2\u4F53\u673A\u7968\u9884\u552E\u670D\u52A1\u3002\u9700\u8981\u767B\u5F55\u5417\uFF1F'; // 단체항공권 예매는 로그인 후 서비스 이용이 가능합니다. 로그인하시겠습니까?
                if('' !='customer'){
                    if(confirm(alert_msg_ruquest_login_grp_booking)){

                        $.ajax({
                            url : "/ajax/booking/setChooseItineraryParameters" // ajax url
                            , dataType : 'json' // ajax 통신의 데이터 형식
                            , async: true // 동기(false):비동기(true)
                            , type : 'post'
                            , data : frm.serialize()
                            , success : function(data){

                                // console.log(data);

                                /**
                                 * 여정 및 번들정보 세션에 저장 후 로그인 화면으로 이동
                                 */
                                frm.find('input[name="returnUrl"]').remove();
                                frm.find('input[name="returnSubmitType"]').remove();
                                frm.append('<input type="hidden" name="returnUrl" class="rqParam" value="/app/booking/groupBookingLoginLanding"/>');
                                frm.append('<input type="hidden" name="returnSubmitType" class="rqParam" value="POST"/>');

                                // loading
                                frm.attr('action','/app/login/memberLogin').submit();
                                beginLoadingAnimation();

                            }
                            , error : function(xhr, status, error){
                                var error_confirm=confirm('\u4F20\u9001\u6570\u636E\u8D44\u6599\u53D1\u751F\u9519\u8BEF\u3002\u70B9\u51FB\u786E\u8BA4\u952E\u9875\u9762\u5C06\u5237\u65B0\u3002');
                                if(error_confirm==true){
                                    document.location.reload();
                                }
                            }
                        });

                    }
                }
                /**
                 * 로그인 상태라면 단체예약 1일 2건 제한 상태 확인
                 * /ajax/booking/getGroupBookingCount
                 */
                else{

                    $.ajax({
                        url: "/ajax/booking/getGroupBookingCount" // ajax url
                        , dataType: 'json' // ajax 통신의 데이터 형식
                        , async: true // 동기(false):비동기(true)
                        , type: 'post'
                        , data : frm.serialize()
                        , success: function (data) {


                            if (data.data.cnt >= 2) {
                                alert('\u56E2\u4F53\u673A\u79681\u65E5\u53EA\u80FD\u9884\u552E2\u6B21\u3002'); // 단체항공권 예매는 1일 2회까지만 가능합니다.
                            }
                            else{
                                frm.submit();
                                beginLoadingAnimation();
                            }

                        }
                        , error: function (xhr, status, error) {
                            var error_confirm = confirm('\u4F20\u9001\u6570\u636E\u8D44\u6599\u53D1\u751F\u9519\u8BEF\u3002\u70B9\u51FB\u786E\u8BA4\u952E\u9875\u9762\u5C06\u5237\u65B0\u3002');
                            if (error_confirm == true) {
                                document.location.reload();
                            }
                        }
                    });
                }


            }else{
                frm.submit();
                beginLoadingAnimation();
            }
        };

        /**
         * 다구간여정 출/도착지, 출발일 선택
         */
        var selectMultiTripAirport = function(obj, itineraryNumber, searchType, layerType){

            currentItineraryNumber = itineraryNumber;
            var i = itineraryNumber-1;

            if('date'==searchType && $('input[name="availabilitySearches['+i+'].depAirport"]').val()!=''
                && $('input[name="availabilitySearches['+i+'].arrAirport"]').val()!=''){
                callBackArrivalAirportConfirm(itineraryNumber);
            }
            else{
                gnbSelectAirport(obj, itineraryNumber, layerType);
            }
        };




        /**
         * 출/도착지 정보의 노출정보 TEXT 정리
         */
        var airportDisplayText = function(el){

            var text = el['city'];
            if(el['city']!=el['airport']){
                text += '/'+el['airport'];
            }
            // text += ' '+el['airport_code'];
            return text;
        };





        /**
         * 나이계산기
         */
        var alert_msg_select_route = '\u8BF7\u5148\u9009\u62E9\u822A\u7EBF\u4E0E\u51FA\u53D1\u65E5\u3002'; // 노선과 출발일을 먼저 선택해주세요.
        var howOldAreYou = function(){

            var depAirport = $('input[name="availabilitySearches[0].depAirport"]').val();
            var arrAirport = $('input[name="availabilitySearches[0].arrAirport"]').val();
            var flightDate = $('input[name="availabilitySearches[0].flightDate"]').val();

            if(depAirport!='' && arrAirport!='' && flightDate!=''){

                flightDate = flightDate.replace(/\-/g,"");

                ageCalculater(flightDate, depAirport, arrAirport);
            }
            else{
                alert(alert_msg_select_route);
            }
        };

        /**
         * 프로모션코드 유효성 검사
         */

        $(document).ready(function(){
            $('div.code input[name="promoCode"]').change(function(){
                $("input[name='validPromoCode']").val('N');
                $('input[name="promoCodeDetails.promoCode"]').val('');
            });
        });
        
        $('.txt_tooltip').on('click', function() {
            $('.discountCodeRule_area').empty();
            var alert_msg_promocode_required = '\u8BF7\u8F93\u5165\u4FC3\u9500\u4EE3\u7801\u3002';//'프로모션코드를 입력해 주세요.';

            var promoCode = $('div.code input[name="promoCode"]').val();

            if(promoCode==''){
                alert(alert_msg_promocode_required);
                $('div.code input[name="promoCode"]').focus();
                return false;
            }
            else{
                discountCodeInfo(promoCode);
                $(this).parents().find('.tooltip_layer.txt').fadeToggle(150);
            }
        });
        
        $('.tooltip_layer.txt.checked').on('click', function() {
                $(this).parents().find('.tooltip_layer.txt').fadeToggle(150);
        });

        /**
         * 입력한 할인코드 안내
         * @param promoCode
         */
        var discountCodeInfo = function(promoCode){

            if(promoCode == ''){
                var alert_msg_promocode_required = '\u8BF7\u8F93\u5165\u4FC3\u9500\u4EE3\u7801\u3002';//'프로모션코드를 입력해 주세요.';
                alert(alert_msg_promocode_required);
                return false;
            } else {
                var alert_msg_check_promocode = '\u8BF7\u786E\u8BA4\u5DF2\u8F93\u5165\u4FC3\u9500\u4EE3\u7801\u7684\u6253\u6298\u89C4\u5B9A\u3002'; // '입력하신 프로모션코드의 할인규정을 확인해주세요.';
                appendLayer('discount_code_rule');
                $.ajax({
                    url : '/ajax/layerComponents/discountCodeRule', // ajax url
                    dataType : 'json', // ajax 통신의 데이터 형식
                    async : true,  // 동기(false):비동기(true)
                    type : 'get',
                    data : {
                        promoCode:promoCode
                    },
                    success : function(data){
                        // console.log(data);
                        if(data.success){
                            $('.discountCodeRule_area').html(data.data.promocode.promoExplain);
                        } else {
                            $('.discountCodeRule_area').html('\u6CA1\u6709\u67E5\u8BE2\u7ED3\u679C');
                        }
                    }
                });
            }
        };

        /**
         * 입력한 할인코드의 유효성 확인
         */
        var callbackDiscountCode = function(useYn){

            $("input[name='validPromoCode']").val(useYn);

            if(useYn != 'Y'){
                $('div.code input[name="promoCode"]').val('').focus();
            }
            else{
                var promoCode = $('div.code input[name="promoCode"]').val();
                $('input[name="promoCodeDetails.promoCode"]').val(promoCode);
            }
        };



        //--
        //-- 시작 -  출/도착공항 선택, 여정선택 레이어 control
        //--

        /**
         * 출발 공항 선택 레이어 호출
         * itineraryNumber ; 여정구간번호, 왕복/편도는 parameter 넘어오지 않음.
         * layerType ; search 검색, region 전체지역
         */
        var gnbSelectAirportObj;
        var gnbSelectAirportLayerType;
        var selectItineraryNumber;
        var gnbSelectAirport = function(obj, itineraryNumber, layerType){

            var alert_msg_select_departure = '\u8BF7\u9009\u62E9\u51FA\u53D1\u57CE\u5E02\u3002';//'출발지를 선택하세요.';

            gnbSelectAirportObj = obj;
            selectItineraryNumber = itineraryNumber;
            gnbSelectAirportLayerType = layerType;

            // console.log(gnbSelectAirportObj);
            // console.log($(gnbSelectAirportObj));

            $('#schedule_calendar').remove();

            /**
             * 출발지, 도착지 검색 영역에 포커스가 있는 경우 레이어 닫히지 않게 처리
             */
            var focusEle = $(":focus");

            // 출발지 선택중
            if( (focusEle.tagName == 'INPUT' && $(focusEle).hasClass('booking') && $(focusEle).hasClass('start'))
            || $(gnbSelectAirportObj).hasClass('booking') && $(gnbSelectAirportObj).hasClass('start') ){
                $('#route_departure').remove();
                $('#route_arrival').remove();
                $('#route_arrival_search').remove();
                $('#schedule_calendar').remove();

                if($('#route_departure_search').length > 0){
                    return false;
                }
            }


            // 도착지 선택중
            if( (focusEle.tagName == 'INPUT' && $(focusEle).hasClass('booking') && $(focusEle).hasClass('end'))
                || $(gnbSelectAirportObj).hasClass('booking') && $(gnbSelectAirportObj).hasClass('end') ){
                $('#route_arrival').remove();
                $('#route_departure').remove();
                $('#route_departure_search').remove();
                $('#schedule_calendar').remove();

                if($('#route_arrival_search').length > 0){
                    return false;
                }
            }


            var deptAirportCode = $('input[name="availabilitySearches[0].depAirport"]').val();


            // 다구간의 경우 해당 구간의 출발공항
            if( typeof itineraryNumber != 'undefined' && itineraryNumber > 0){
                itineraryNumber = parseInt(itineraryNumber,10);
                deptAirportCode = $('input[name="availabilitySearches['+(itineraryNumber-1)+'].depAirport"]').val();
            }

            // 위치 확인
            var $this = $(obj),
                thisTop = $this.offset().top - $('div.main_booking_inside').offset().top + 65,
                thisLeft = $this.offset().left - $('div.main_booking_inside').offset().left;

            if(layerType == 'region'){

                if(deptAirportCode!='' && $(obj).hasClass('end')){
                    gnbRouteArrival(deptAirportCode, $('input[name="tripType"]:checked').val(), itineraryNumber);
                    $('#route_arrival').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
                    showLayer('route_arrival');
                }
                else if(deptAirportCode=='' && $(obj).hasClass('end')){
                    $(obj).blur();
                    alert(alert_msg_select_departure);
                    return false;
                }
                else{
                    gnbRouteDeparture($('input[name="tripType"]:checked').val(), undefined, itineraryNumber);
                    $('#route_departure').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
                    showLayer('route_departure');

                }

            }
            else if(layerType == 'search'){

                if(deptAirportCode!='' && $(obj).hasClass('end')){
                    gnbRouteArrivalSearch(obj, deptAirportCode, $('input[name="tripType"]:checked').val(), itineraryNumber);
                    $('#route_arrival_search').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
                    showLayer('route_arrival_search');
                }
                else if(deptAirportCode=='' && $(obj).hasClass('end')){
                    $(obj).blur();
                    alert(alert_msg_select_departure);
                    return false;
                }
                else{
                    gnbRouteDepartureSearch(obj, $('input[name="tripType"]:checked').val(), undefined, itineraryNumber);
                    $('#route_departure_search').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
                    $('#route_departure').remove();
                    showLayer('route_departure_search');
                }


            }

        };


        /**
         * 출발공항 선택 레이어의 callback function
         */
        var gnbCallBackDepartureAirport = function(el, itineraryNumber){

            if( typeof itineraryNumber == 'undefined'){
                itineraryNumber = 1;
            }

            /**
             * 시작 - #1217 [PC홈페이지] 항공권예매>운임 조회 출발 공항 변경시 도착 공항 초기화 요청
             */
            // form 정보 삭제
            $('input[name="availabilitySearches['+(currentItineraryNumber-1)+'].arrAirport"]').val('');

            /**
             * 끝 - #1217 [PC홈페이지] 항공권예매>운임 조회 출발 공항 변경시 도착 공항 초기화 요청
             */

            /*
            $(el).data('city'); // 도시
            $(el).data('airport'); // 공항
            $(el).data('airport_code'); // 공항코드
            $(el).data('conti'); // 대륙코드
            */

            // alert($('#tripType_RT:checked').length +'/'+$('#tripType_OW:checked').length +'/'+$('#tripType_MC:checked').length);

            // 선택값 저장 - 왕복인경우
            if($('#tripType_RT:checked').length==1){
                // 구간1 출발
                setAirportData($('input[name="availabilitySearches[0].depAirport"]'),el);

                // 구간2 도착
                setAirportData($('input[name="availabilitySearches[1].arrAirport"]'),el);
            }
            // 편도인경우
            else if($('#tripType_OW:checked').length==1){
                // 구간1 출발
                setAirportData($('input[name="availabilitySearches[0].depAirport"]'),el);
            }
            // 다구간인경우
            else if($('#tripType_MC:checked').length==1){
                // 구간별 출발
                setAirportData($('input[name="availabilitySearches['+(currentItineraryNumber-1)+'].depAirport"]'),el);
            }

            // display, 출발지 텍스트
            var departureAirport = $(el).data('city');
            if(departureAirport!=$(el).data('airport')){
                departureAirport += '/'+$(el).data('airport');
            }


            // 편도,왕복
            // if($('#tripType_RT:checked').length==1 || $('#tripType_OW:checked').length==1) {
                $('#main_reser01 div.start').addClass('focus');
                $('#main_reser01 div.start div.selected_area').addClass('on');
                $('#main_reser01 div.start div.selected_area').find('span.area').text(departureAirport);
                $('#main_reser01 div.start div.selected_area').find('span.eng').text($(el).data('airport_code'));

                $('#main_reser02 div.start').addClass('focus');
                $('#main_reser02 div.start div.selected_area').addClass('on');
                $('#main_reser02 div.start div.selected_area').find('span.area').text(departureAirport);
                $('#main_reser02 div.start div.selected_area').find('span.eng').text($(el).data('airport_code'));
            // }
            // 다구간인경우
            // else if($('#tripType_MC:checked').length==1){
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.start div.selected_area').addClass('on');
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.start div.selected_area').find('span.area').text(departureAirport);
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.start div.selected_area').find('span.eng').text($(el).data('airport_code'));
            // }


            /**
             * 시작 - #1217 [PC홈페이지] 항공권예매>운임 조회 출발 공항 변경시 도착 공항 초기화 요청
             */
            // 화면 display 정보 삭제
            $('#main_reser01 div.end').removeClass('focus');
            $('#main_reser01 div.end div.selected_area').removeClass('on');

            $('#main_reser02 div.end').removeClass('focus');
            $('#main_reser02 div.end div.selected_area').removeClass('on');

            // 왕복, 편도 출발지 선택시 다구간 구간2 부터의 정보는 모두 삭제
            if($('#tripType_RT:checked').length==1 || $('#tripType_OW:checked').length==1) {


                for(var it=1 ; it<=4 ; it++){
                    if(it>1) {
                        $('#itinerary_multi_trip_' + it).find('div.start').removeClass('focus');
                        $('#itinerary_multi_trip_' + it).find('div.start div.selected_area').removeClass('on');
                    }

                    $('#itinerary_multi_trip_' + it).find('div.end').removeClass('focus');
                    $('#itinerary_multi_trip_' + it).find('div.end div.selected_area').removeClass('on');
                }
            }


            /**
             * 끝 - #1217 [PC홈페이지] 항공권예매>운임 조회 출발 공항 변경시 도착 공항 초기화 요청
             */

            // 도착지 공항 검색으로 레이어 전환

            // 검색 input box 초기화
            $(gnbSelectAirportObj).val('');

            // 위치 확인
            var obj = $(gnbSelectAirportObj).parents('div.booking_wrap').find('input.booking.end');
            gnbSelectAirportObj = obj;

            // 위치 확인
            var $this = $(obj),
                thisTop = $this.offset().top - $('div.main_booking_inside').offset().top + 65,
                thisLeft = $this.offset().left - $('div.main_booking_inside').offset().left;

            if(gnbSelectAirportLayerType == 'region'){

                gnbRouteArrival($(el).data('airport_code'), $('input[name="tripType"]:checked').val(), itineraryNumber);
                showLayer('route_arrival','route_departure', true);
                $('#route_arrival').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
            }
            else if(gnbSelectAirportLayerType == 'search'){
                obj.focus();
                obj.parents('div.input_wrap').find('div.selected_area').removeClass('on');
                gnbRouteArrivalSearch(obj, $(el).data('airport_code'), $('input[name="tripType"]:checked').val(), itineraryNumber);
                showLayer('route_arrival_search','route_departure_search', true);
                $('#route_arrival_search').css({'position': 'absolute','top': thisTop, 'left': thisLeft});
            }

        };

        /**
         * 도착공항 선택 레이어의 callback function
         */
        var gnbCallBackArrivalAirport = function(el){

            // 검색 input box 초기화
            $(gnbSelectAirportObj).val('');

            // 선택값 저장 - 왕복인경우
            if($('#tripType_RT:checked').length==1){
                // 구간1 도착
                setAirportData($('input[name="availabilitySearches[0].arrAirport"]'),el);

                // 구간2 출발
                setAirportData($('input[name="availabilitySearches[1].depAirport"]'),el);
            }
            // 편도인경우
            else if($('#tripType_OW:checked').length==1){
                // 구간1 도착
                setAirportData($('input[name="availabilitySearches[0].arrAirport"]'),el);

            }
            // 다구간인경우
            else if($('#tripType_MC:checked').length==1){
                // 구간별 도착
                setAirportData($('input[name="availabilitySearches['+(currentItineraryNumber-1)+'].arrAirport"]'),el);
            }

            // display, 공항 정보 표출
            var arrivalAirport = $(el).data('city');
            if(arrivalAirport!=$(el).data('airport')){
                arrivalAirport += '/'+$(el).data('airport');
            }

            // display, 편도,왕복
            // if($('#tripType_RT:checked').length==1 || $('#tripType_OW:checked').length==1) {
                $('#main_reser01 div.input_wrap.end').addClass('focus');
                $('#main_reser01 div.input_wrap.end div.selected_area').addClass('on');
                $('#main_reser01 div.input_wrap.end div.selected_area').find('span.area').text(arrivalAirport);
                $('#main_reser01 div.input_wrap.end div.selected_area').find('span.eng').text($(el).data('airport_code'));

                $('#main_reser02 div.input_wrap.end').addClass('focus');
                $('#main_reser02 div.input_wrap.end div.selected_area').addClass('on');
                $('#main_reser02 div.input_wrap.end div.selected_area').find('span.area').text(arrivalAirport);
                $('#main_reser02 div.input_wrap.end div.selected_area').find('span.eng').text($(el).data('airport_code'));
            // }
            // 다구간인경우
            // else if($('#tripType_MC:checked').length==1){
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.end').addClass('focus');
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.end div.selected_area').addClass('on');
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.end div.selected_area').find('span.area').text(arrivalAirport);
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.end div.selected_area').find('span.eng').text($(el).data('airport_code'));
            // }


        };

        /**
         * 출/도착 공항정보 선택시 data 및 value 저장
         */
        var setAirportData = function (airportObj, el){
            $(airportObj).data('city',$(el).data('city'));
            $(airportObj).data('airport',$(el).data('airport'));
            $(airportObj).data('airport_code',$(el).data('airport_code'));
            $(airportObj).data('conti',$(el).data('conti'));
            airportObj.val($(el).data('airport_code'));
        };


        /**
         * 도착공항 선택 레이어의 '확인'버튼 클릭 callback function
         */
        var gnbCallBackArrivalAirportConfirm = function(itineraryNumber){

            var i=0;
            var calendarInpurObj;
            var alert_msg_choose_departure_airport = '\u8BF7\u9009\u62E9\u51FA\u53D1\u57CE\u5E02\u3002';//'출발지를 선택해주세요.';
            var alert_msg_choose_arrival_airport = '\u8BF7\u9009\u62E9\u5230\u8FBE\u57CE\u5E02\u3002';//'도착지 공항을 선택해주세요.';

            if( typeof itineraryNumber != 'undefined'){

                currentItineraryNumber = itineraryNumber;

                if(itineraryNumber>0){
                    i = itineraryNumber-1;
                }
            }

            // 출,도착 공항이 선택되지 않은경우 출발공항 선택 레이어를 호출합니다.

            // 왕복
            if($('#tripType_RT:checked').length==1) {

                calendarInpurObj = $('#main_reser01 a.btn_date');

                if($('input[name="availabilitySearches['+i+'].depAirport"]').val()==''){
                	alert(alert_msg_choose_departure_airport);
                	$('#main_reser01 input.booking.start').trigger('click');
                    $('#main_reser01 input.booking.start').focus();
                    return;
                }
                else if($('input[name="availabilitySearches['+i+'].arrAirport"]').val()==''){
                	alert(alert_msg_choose_arrival_airport);
                	$('#main_reser01 input.booking.end').trigger('click');
                    $('#main_reser01 input.booking.end').focus();
                    return;
                }


            }
            // 편도
            else if($('#tripType_OW:checked').length==1) {

                calendarInpurObj = $('#main_reser02 a.btn_date');

                if($('input[name="availabilitySearches['+i+'].depAirport"]').val()==''){
                	alert(alert_msg_choose_departure_airport);
                	$('#main_reser02 input.booking.start').trigger('click');
                    $('#main_reser02 input.booking.start').focus();
                    return;
                }
                else if($('input[name="availabilitySearches['+i+'].arrAirport"]').val()==''){
                	alert(alert_msg_choose_arrival_airport);
                	$('#main_reser02 input.booking.end').trigger('click');
                    $('#main_reser02 input.booking.end').focus();
                    return;
                }
            }
            // 다구간인경우
            else if($('#tripType_MC:checked').length==1){

                calendarInpurObj = $('#itinerary_multi_trip_' + itineraryNumber+' a.btn_date');

                if($('input[name="availabilitySearches['+i+'].depAirport"]').val()==''){
                	alert(alert_msg_choose_departure_airport);
                	$('#itinerary_multi_trip_' + itineraryNumber+' input.booking.start').trigger('click');
                    $('#itinerary_multi_trip_' + itineraryNumber+' input.booking.start').focus();
                    return;
                }
                else if($('input[name="availabilitySearches['+i+'].arrAirport"]').val()==''){
                	alert(alert_msg_choose_arrival_airport);
                	$('#itinerary_multi_trip_' + itineraryNumber+' input.booking.end').trigger('click');
                    $('#itinerary_multi_trip_' + itineraryNumber+' input.booking.end').focus();
                    return;
                }

            }


            // 일정선택 레이어 전환
            var tripType = $('input[name="tripType"]:checked').val();
            var bookingType = $('input[name="bookingType"]:checked').val();
            var currency = 'CNY';
            var depAirport = $('input[name="availabilitySearches['+i+'].depAirport"]').val();
            var arrAirport = $('input[name="availabilitySearches['+i+'].arrAirport"]').val();
            gnbScheduleCalendar(tripType, bookingType, currency, depAirport, arrAirport);

            $('#route_arrival_search').remove();
            showLayer('schedule_calendar','route_arrival', true);

            // 위치 확인
            var $this = $(calendarInpurObj),
                thisTop = $this.offset().top - $('div.main_booking_inside').offset().top + 65,
                thisLeft = 0;

            $('#schedule_calendar').css({'position': 'absolute','top': thisTop, 'left': thisLeft});

        };

        /**
         * 일정선택 레이어의 확인버튼 이벤트 처리 callback function
         * @param schedule      array형태로 반환, 편도/다구간조회인 경우 size=1, 왕복인경우 size=2, YYYYMMDD
         * @param schedule_str  YYYY-MM-DD
         */
        var gnbCallBackScheduleConfirm = function(schedule, schedule_str){


            //왕복
            if($('#tripType_RT:checked').length==1) {

                $('#main_reser01 div.date').addClass('focus');
                $('#main_reser01 div.date input').eq(0).val(schedule_str[0]);
                $('#main_reser01 div.date input').eq(1).val(schedule_str[1]);


                $('#main_reser02 div.date').addClass('focus');
                $('#main_reser02 div.date input').eq(0).val(schedule_str[0]);

                // RQ
                $('input[name="availabilitySearches[0].flightDate"]').val(schedule_str[0]);
                $('input[name="availabilitySearches[1].flightDate"]').val(schedule_str[1]);
            }
            // 편도
            else if($('#tripType_OW:checked').length==1) {

                $('#main_reser01 div.date').addClass('focus');
                $('#main_reser01 div.date input').eq(0).val(schedule_str[0]);

                $('#main_reser02 div.date').addClass('focus');
                $('#main_reser02 div.date input').eq(0).val(schedule_str[0]);

                // RQ
                $('input[name="availabilitySearches[0].flightDate"]').val(schedule_str[0]);

            }
            // 다구간인경우
            else if($('#tripType_MC:checked').length==1){
                // display
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.date').addClass('on');
                $('#itinerary_multi_trip_' + currentItineraryNumber).find('div.date input').val(schedule_str[0]);

                // $('#itinerary_multi_trip_' + currentItineraryNumber).find('input[name="departure_date"]').val(schedule_str[0]);

                // RQ
                $('input[name="availabilitySearches['+(currentItineraryNumber-1)+'].flightDate"]').val(schedule_str[0]);
            }

            showLayer('wrap', 'schedule_calendar', true);
        };

        /**
         * 호출된 레이어에서 사용자 요청에 의해 프로세스 중단(창닫기)시 부모페이어를 재호출
         */
        var callBackOpener = function(hideLayerName){
            // $('#'+hideLayerName).remove();

            $('#wrap').slideDown( "slow", function() {
                $('#'+hideLayerName).remove();
            });

            // $('#wrap').css('overflow','');
            $('body').removeClass('no_scroll');
        };


        //--
        //-- 끝 -  출/도착공항 선택, 여정선택 레이어 control
        //--


        //--------------- from global.js

        /**
         * 여정선택 출/도착일 선택하는 캘린더 레이어 호출
         * @param tripType
         * @param deptAirportCode
         * @param arriAirportCode
         */
        var gnbScheduleCalendar = function(tripType, bookingType, currency, deptAirportCode, arriAirportCode){

            scheduleCalendar(tripType, bookingType, currency, deptAirportCode, arriAirportCode);

            // gnb job flag
            isGnbRequest = true;

        };


        /**
         * 출발 공항선택 - 전체지역
         * @param tripType
         */
        var gnbRouteDeparture = function(tripType, deptAirportCode, itineraryNumber){

            routeDeparture(tripType, deptAirportCode, itineraryNumber);

            // gnb job flag
            isGnbRequest = true;

        };


        /**
         * 출발 공항선택 - 검색
         * @param tripType
         */
        var gnbRouteDepartureSearch = function(obj, tripType, deptAirportCode, itineraryNumber){

            routeDepartureSearch(obj, tripType, deptAirportCode, itineraryNumber);

            // gnb job flag
            isGnbRequest = true;

        };


        /**
         * 도착 공항선택 - 전체지역
         * @param deptAirportCode
         * @param tripType
         */
        var gnbRouteArrival = function(deptAirportCode, tripType, itineraryNumber){

            routeArrival(deptAirportCode, tripType, itineraryNumber);

            // gnb job flag
            isGnbRequest = true;

        };


        /**
         * 도착 공항선택 - 검색
         * @param deptAirportCode
         * @param tripType
         */
        var gnbRouteArrivalSearch = function(obj, deptAirportCode, tripType, itineraryNumber){

            routeArrivalSearch(obj, deptAirportCode, tripType, itineraryNumber);

            // gnb job flag
            isGnbRequest = true;

        };


        //--------------- end global.js


        /**
         * 저장된 RQ가 있는경우 정보 표출
         */
        $(document).ready(function(){
            reformAirAvailabilityRQInfo();
        });

        var reformAirAvailabilityRQInfo = function(){

            // $('#display_tripType_'+$('#airAvailabilityRQ input[name="tripType"]:checked').val()).parents('a.setTripType').click().click();

            $.each($('div.sel_section input[name="tripTypeButton"]'),function(){

                if($('#airAvailabilityRQ input[name="tripType"]:checked').val()=='MC'){
                    $('#airAvailabilityRQ input[name="tripType"]').eq(0).prop('checked',true);
                }

                if($(this).val()==$('#airAvailabilityRQ input[name="tripType"]:checked').val()){
                    $(this).prop('checked', true);
                    $('#display_tripType_'+$(this).val()).parents('a.setTripType').click();
                }
            });

            // checkTripType();


            // 노선정보
            if($('input[name="availabilitySearches[0].depAirport"]').val()!='' && $('input[name="availabilitySearches[0].arrAirport"]').val()!=''){

                $('#main_reser01 div.start').addClass('focus');
                $('#main_reser01 div.start div.selected_area').addClass('on');
                $('#main_reser01 div.start div.selected_area').find('span.area').text($('input[name="availabilitySearches[0].depAirportName"]').val());
                $('#main_reser01 div.start div.selected_area').find('span.eng').text($('input[name="availabilitySearches[0].depAirport"]').val());

                $('#main_reser01 div.end').addClass('focus');
                $('#main_reser01 div.end div.selected_area').addClass('on');
                $('#main_reser01 div.end div.selected_area').find('span.area').text($('input[name="availabilitySearches[0].arrAirportName"]').val());
                $('#main_reser01 div.end div.selected_area').find('span.eng').text($('input[name="availabilitySearches[0].arrAirport"]').val());


                $('#main_reser02 div.start').addClass('focus');
                $('#main_reser02 div.start div.selected_area').addClass('on');
                $('#main_reser02 div.start div.selected_area').find('span.area').text($('input[name="availabilitySearches[0].depAirportName"]').val());
                $('#main_reser02 div.start div.selected_area').find('span.eng').text($('input[name="availabilitySearches[0].depAirport"]').val());

                $('#main_reser02 div.end').addClass('focus');
                $('#main_reser02 div.end div.selected_area').addClass('on');
                $('#main_reser02 div.end div.selected_area').find('span.area').text($('input[name="availabilitySearches[0].arrAirportName"]').val());
                $('#main_reser02 div.end div.selected_area').find('span.eng').text($('input[name="availabilitySearches[0].arrAirport"]').val());

            }

            // 탑승일 정보
            if($('input[name="availabilitySearches[0].flightDate"]').val()!=''){

                $('#main_reser01 div.input_wrap.date').addClass('focus');
                $('#main_reser01 input.booking.date').eq(0).val($('input[name="availabilitySearches[0].flightDate"]').val());
                $('#main_reser01 input.booking.date').eq(1).val($('input[name="availabilitySearches[1].flightDate"]').val());

                if($('input[name="availabilitySearches[1].flightDate"]').val()!=''){
                    $('#main_reser01 input.booking.date').eq(0).val($('input[name="availabilitySearches[0].flightDate"]').val());
                }


                $('#main_reser02 div.input_wrap.date').addClass('focus');
                $('#main_reser02 input.booking.date').eq(0).val($('input[name="availabilitySearches[0].flightDate"]').val());
                $('#main_reser02 input.booking.date').eq(1).val($('input[name="availabilitySearches[1].flightDate"]').val());

                if($('input[name="availabilitySearches[1].flightDate"]').val()!=''){
                    $('#main_reser02 input.booking.date').eq(0).val($('input[name="availabilitySearches[0].flightDate"]').val());
                }

            }


            // 다구간인경우
            for(var i=0 ; i<4 ; i++){
                // 노선정보
                if($('input[name="availabilitySearches['+i+'].depAirport"]').val()!='' && $('input[name="availabilitySearches['+i+'].arrAirport"]').val()!=''){

                    if(i>1){
                        multiTripItineraryCount = i+1;
                    }

                    $('#itinerary_multi_trip_'+(i+1)+' div.start').addClass('focus');
                    $('#itinerary_multi_trip_'+(i+1)+' div.start div.selected_area').find('span.eng').text($('input[name="availabilitySearches['+i+'].depAirport"]').val());
                    $('#itinerary_multi_trip_'+(i+1)+' div.start div.selected_area').find('span.area').text($('input[name="availabilitySearches['+i+'].depAirportName"]').val());
                    $('#itinerary_multi_trip_'+(i+1)+' div.start div.selected_area').addClass('on');

                    $('#itinerary_multi_trip_'+(i+1)+' div.end').addClass('focus');
                    $('#itinerary_multi_trip_'+(i+1)+' div.end div.selected_area').find('span.eng').text($('input[name="availabilitySearches['+i+'].arrAirport"]').val());
                    $('#itinerary_multi_trip_'+(i+1)+' div.end div.selected_area').find('span.area').text($('input[name="availabilitySearches['+i+'].arrAirportName"]').val());
                    $('#itinerary_multi_trip_'+(i+1)+' div.end div.selected_area').addClass('on');


                    // 탑승일 정보
                    $('#itinerary_multi_trip_'+(i+1)+' input.booking.date').val($('input[name="availabilitySearches['+i+'].flightDate"]').val());
                    $('#itinerary_multi_trip_'+(i+1)+' div.input_wrap.date').addClass('focus');

                    $('#itinerary_multi_trip_'+(i+1)).show();



                    // TODO delete , old html
                    $('#itinerary_multi_trip_'+(i+1)).find('input[name="origin_name"]').val($('input[name="availabilitySearches['+i+'].depAirportName"]').val()
                        + ' ' + $('input[name="availabilitySearches['+i+'].depAirport"]').val());

                    $('#itinerary_multi_trip_'+(i+1)).find('input[name="destination_name"]').val($('input[name="availabilitySearches['+i+'].arrAirportName"]').val()
                        + ' ' + $('input[name="availabilitySearches['+i+'].arrAirport"]').val());
                    // -- TODO delete , old html

                }



                // -- TODO delete , old html
                $('#itinerary_multi_trip_'+(i+1)).find('input[name="departure_date"]').val($('input[name="availabilitySearches['+i+'].flightDate"]').val());
                // -- TODO delete , old html

            }


        };



        $(function(){

            $('#route_departure_search, #route_departure').on('focusout', function() {
                $('.focus_start2').focus();
                $(this).remove();
            });

            $('#route_arrival_search, #route_arrival').on('focusout', function() {
                $('.focus_end2').focus();
                $(this).remove();
            });

            $('#schedule_calendar').on('focusout', function() {
                $('.focus_date3').focus();
                $(this).remove();
            });

        });


    