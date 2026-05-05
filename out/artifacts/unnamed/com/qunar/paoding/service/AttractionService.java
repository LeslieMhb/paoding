package com.qunar.paoding.service;

import com.qunar.paoding.model.dto.*;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

/**
 * 景点服务 - Mock实现
 */
@Service
public class AttractionService {

    public AttractionListResult searchAttractions(AttractionQueryRequest request) {
        List<AttractionInfo> attractions = buildMockAttractions(request.getArrival());
        return AttractionListResult.builder()
                .attractionList(attractions)
                .recommendTitle("为您推荐" + request.getArrival() + "热门景点")
                .recommendSubTitle(request.getArrival() + "必游景点TOP" + attractions.size())
                .build();
    }

    public RoutePlanResult planRoute(AttractionQueryRequest request) {
        return buildMockRoutePlan(request.getArrival(), request.getDays());
    }

    private List<AttractionInfo> buildMockAttractions(String city) {
        return Arrays.asList(
                AttractionInfo.builder()
                        .sightId("sight_001")
                        .title("西湖")
                        .imageUrl("https://img.qunarzz.com/p/sight/001.jpg")
                        .selected(true)
                        .detail(AttractionInfo.AttractionDetail.builder()
                                .title("西湖风景名胜区")
                                .subtitle("5A级景区 · 世界文化遗产")
                                .imageUrlList(Arrays.asList(
                                        "https://img.qunarzz.com/p/sight/001_1.jpg",
                                        "https://img.qunarzz.com/p/sight/001_2.jpg"
                                ))
                                .description("西湖位于杭州市区西面，是中国大陆首批国家重点风景名胜区和中国十大风景名胜之一。三面环山，面积约6.39平方千米，湖中有三岛，以'一山、二塔、三岛、三堤、五湖'为基本格局。")
                                .tips(Arrays.asList("建议游览时间3-4小时", "苏堤春晓和断桥残雪是必打卡景点", "可乘坐游船游览湖中三岛"))
                                .build())
                        .build(),
                AttractionInfo.builder()
                        .sightId("sight_002")
                        .title("灵隐寺")
                        .imageUrl("https://img.qunarzz.com/p/sight/002.jpg")
                        .selected(true)
                        .detail(AttractionInfo.AttractionDetail.builder()
                                .title("灵隐飞来峰景区")
                                .subtitle("5A级景区 · 千年古刹")
                                .imageUrlList(Arrays.asList(
                                        "https://img.qunarzz.com/p/sight/002_1.jpg",
                                        "https://img.qunarzz.com/p/sight/002_2.jpg"
                                ))
                                .description("灵隐寺又名云林寺，位于杭州西湖灵隐山麓，背靠北高峰，面朝飞来峰，始建于东晋咸和元年（326年），是中国佛教著名十刹之一。飞来峰石刻造像是中国南方石窟艺术的瑰宝。")
                                .tips(Arrays.asList("建议游览时间2-3小时", "飞来峰造像不容错过", "初一十五人流量较大"))
                                .build())
                        .build(),
                AttractionInfo.builder()
                        .sightId("sight_003")
                        .title("西溪湿地")
                        .imageUrl("https://img.qunarzz.com/p/sight/003.jpg")
                        .selected(false)
                        .detail(AttractionInfo.AttractionDetail.builder()
                                .title("西溪国家湿地公园")
                                .subtitle("5A级景区 · 城市湿地公园")
                                .imageUrlList(Arrays.asList(
                                        "https://img.qunarzz.com/p/sight/003_1.jpg",
                                        "https://img.qunarzz.com/p/sight/003_2.jpg"
                                ))
                                .description("西溪湿地是中国首个国家湿地公园，总面积约11.5平方公里。这里生态资源丰富、自然景观幽雅，有'三堤十景'之称，是城市中难得的湿地景观。")
                                .tips(Arrays.asList("建议游览时间4-5小时", "推荐乘坐摇橹船深度游览", "秋季火柿映波最具特色"))
                                .build())
                        .build(),
                AttractionInfo.builder()
                        .sightId("sight_004")
                        .title("千岛湖")
                        .imageUrl("https://img.qunarzz.com/p/sight/004.jpg")
                        .selected(false)
                        .detail(AttractionInfo.AttractionDetail.builder()
                                .title("千岛湖风景区")
                                .subtitle("5A级景区 · 天下第一秀水")
                                .imageUrlList(Arrays.asList(
                                        "https://img.qunarzz.com/p/sight/004_1.jpg",
                                        "https://img.qunarzz.com/p/sight/004_2.jpg"
                                ))
                                .description("千岛湖位于杭州市淳安县，湖区拥有1078座翠岛，是世界上岛屿最多的湖。湖水清澈，被誉为'天下第一秀水'，自然风光旖旎，生态环境绝佳。")
                                .tips(Arrays.asList("距杭州市区约2-3小时车程", "建议安排1-2天游览", "梅峰岛是最佳观景点"))
                                .build())
                        .build(),
                AttractionInfo.builder()
                        .sightId("sight_005")
                        .title("宋城")
                        .imageUrl("https://img.qunarzz.com/p/sight/005.jpg")
                        .selected(false)
                        .detail(AttractionInfo.AttractionDetail.builder()
                                .title("宋城景区")
                                .subtitle("4A级景区 · 给我一天还你千年")
                                .imageUrlList(Arrays.asList(
                                        "https://img.qunarzz.com/p/sight/005_1.jpg",
                                        "https://img.qunarzz.com/p/sight/005_2.jpg"
                                ))
                                .description("宋城景区以宋代文化为主题，再现了宋代都市的繁华景象。《宋城千古情》是宋城景区的灵魂演出，被誉为'世界三大名秀'之一，场面宏大，震撼人心。")
                                .tips(Arrays.asList("千古情演出必看，建议提前购票", "景区内有丰富的互动体验项目", "晚上灯光秀别有风味"))
                                .build())
                        .build()
        );
    }

    private RoutePlanResult buildMockRoutePlan(String city, Integer days) {
        if (days == null || days < 1) {
            days = 3;
        }

        RoutePlanResult.DayRoute day1 = RoutePlanResult.DayRoute.builder()
                .day(1)
                .theme("西湖经典之旅")
                .routeText("断桥残雪 → 白堤 → 孤山 → 苏堤春晓 → 花港观鱼 → 雷峰塔")
                .highlights("沿西湖漫步，感受白娘子传说，登雷峰塔俯瞰西湖全景")
                .fullDesc("上午从断桥残雪出发，沿白堤漫步至孤山，参观浙江省博物馆孤山馆区。中午在楼外楼品尝西湖醋鱼等杭帮菜。下午沿苏堤漫步至花港观鱼，傍晚登雷峰塔欣赏西湖日落。")
                .spots(Arrays.asList(
                        RoutePlanResult.PoiSpot.builder().name("断桥残雪").city("杭州").province("浙江").description("白蛇传传说发源地").build(),
                        RoutePlanResult.PoiSpot.builder().name("白堤").city("杭州").province("浙江").description("西湖最著名的堤岸之一").build(),
                        RoutePlanResult.PoiSpot.builder().name("苏堤春晓").city("杭州").province("浙江").description("西湖十景之首").build(),
                        RoutePlanResult.PoiSpot.builder().name("雷峰塔").city("杭州").province("浙江").description("西湖标志性建筑").build()
                ))
                .build();

        RoutePlanResult.DayRoute day2 = RoutePlanResult.DayRoute.builder()
                .day(2)
                .theme("禅意文化之旅")
                .routeText("灵隐寺 → 飞来峰造像 → 永福禅寺 → 梅家坞茶园")
                .highlights("千年古刹祈福，品龙井茶韵，感受杭州茶文化")
                .fullDesc("上午前往灵隐寺参拜，游览飞来峰石刻造像群，欣赏永福禅寺的清幽。中午在灵隐寺素斋馆用餐。下午前往梅家坞茶园，漫步茶园小径，品尝正宗龙井茶，体验茶文化。")
                .spots(Arrays.asList(
                        RoutePlanResult.PoiSpot.builder().name("灵隐寺").city("杭州").province("浙江").description("千年古刹，江南名寺").build(),
                        RoutePlanResult.PoiSpot.builder().name("飞来峰").city("杭州").province("浙江").description("南方石窟艺术瑰宝").build(),
                        RoutePlanResult.PoiSpot.builder().name("梅家坞").city("杭州").province("浙江").description("龙井茶核心产区").build()
                ))
                .build();

        RoutePlanResult.DayRoute day3 = RoutePlanResult.DayRoute.builder()
                .day(3)
                .theme("湿地生态之旅")
                .routeText("西溪湿地 → 河渚街 → 洪园 → 宋城千古情")
                .highlights("摇橹船游览湿地，感受宋城穿越之旅")
                .fullDesc("上午乘摇橹船游览西溪湿地，途经秋芦飞雪、烟水渔庄等景点。中午在河渚街品尝特色小吃。下午游览洪园。傍晚前往宋城，观看《宋城千古情》演出，感受穿越千年的视觉盛宴。")
                .spots(Arrays.asList(
                        RoutePlanResult.PoiSpot.builder().name("西溪湿地").city("杭州").province("浙江").description("城市湿地，生态天堂").build(),
                        RoutePlanResult.PoiSpot.builder().name("宋城").city("杭州").province("浙江").description("穿越千年，感受宋代繁华").build()
                ))
                .build();

        List<RoutePlanResult.DayRoute> routes;
        if (days <= 1) {
            routes = List.of(day1);
        } else if (days == 2) {
            routes = Arrays.asList(day1, day2);
        } else {
            routes = Arrays.asList(day1, day2, day3);
        }

        return RoutePlanResult.builder()
                .title(city + days + "日游经典路线")
                .days(days)
                .dayRouteList(routes)
                .build();
    }
}
