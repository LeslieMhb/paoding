package com.qunar.paoding.service;

import com.qunar.paoding.model.dto.*;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

/**
 * 酒店服务 - Mock实现
 */
@Service
public class HotelService {

    public HotelListResult searchHotels(HotelQueryRequest request) {
        List<HotelInfo> hotels = buildMockHotels(request.getArrCity());
        return HotelListResult.builder()
                .hotelList(hotels)
                .recommendTitle("共找到" + hotels.size() + "家酒店，为您推荐以下精选")
                .recommendSubTitle(request.getArrCity() + "精选酒店")
                .recommendMoreScheme("qunar://hotel/list?city=" + request.getArrCity())
                .build();
    }

    public HotelInfo getHotelDetail(String hotelSeq) {
        return buildMockHotelList().stream()
                .filter(h -> hotelSeq.equals(h.getHotelSeq()))
                .findFirst()
                .orElse(buildMockHotelList().get(0));
    }

    private List<HotelInfo> buildMockHotels(String city) {
        return buildMockHotelList();
    }

    private List<HotelInfo> buildMockHotelList() {
        return Arrays.asList(
                HotelInfo.builder()
                        .hotelName("杭州西湖国宾馆")
                        .hotelSeq("hotel_001")
                        .score(4.8)
                        .price(HotelInfo.HotelPrice.builder().price(128000).currency("CNY").priceDesc("¥1280起").build())
                        .imageUrl("https://img.qunarzz.com/p/hotel/001.jpg")
                        .tagList(Arrays.asList("湖景房", "五星级", "西湖畔"))
                        .hotelAddress("杭州市西湖区杨公堤18号")
                        .locationInfo("西湖景区内")
                        .hotelBriefDesc("坐落于西湖核心景区，独享西湖美景，历史悠久的国宾级酒店")
                        .dangciText("五星级")
                        .dangciImgUrl("https://img.qunarzz.com/p/hotel/star5.png")
                        .recommendation("西湖边最负盛名的国宾馆，景观绝佳")
                        .commentDesc("好评如潮，位置绝佳，服务一流")
                        .hotelDetailScheme("qunar://hotel/detail?seq=hotel_001")
                        .collected(false)
                        .build(),
                HotelInfo.builder()
                        .hotelName("杭州索菲特西湖大酒店")
                        .hotelSeq("hotel_002")
                        .score(4.6)
                        .price(HotelInfo.HotelPrice.builder().price(88000).currency("CNY").priceDesc("¥880起").build())
                        .imageUrl("https://img.qunarzz.com/p/hotel/002.jpg")
                        .tagList(Arrays.asList("湖景房", "豪华型", "近西湖"))
                        .hotelAddress("杭州市上城区西湖大道333号")
                        .locationInfo("距西湖步行5分钟")
                        .hotelBriefDesc("法式优雅与江南韵味的完美结合，紧邻西湖")
                        .dangciText("豪华型")
                        .dangciImgUrl("https://img.qunarzz.com/p/hotel/star4.png")
                        .recommendation("性价比超高的湖景酒店，法式风情")
                        .commentDesc("房间宽敞，湖景房视野极佳")
                        .hotelDetailScheme("qunar://hotel/detail?seq=hotel_002")
                        .collected(false)
                        .build(),
                HotelInfo.builder()
                        .hotelName("杭州西溪悦榕庄")
                        .hotelSeq("hotel_003")
                        .score(4.9)
                        .price(HotelInfo.HotelPrice.builder().price(258000).currency("CNY").priceDesc("¥2580起").build())
                        .imageUrl("https://img.qunarzz.com/p/hotel/003.jpg")
                        .tagList(Arrays.asList("度假", "豪华型", "西溪湿地"))
                        .hotelAddress("杭州市西湖区紫金港路西溪天堂国际旅游综合体")
                        .locationInfo("西溪湿地旁")
                        .hotelBriefDesc("隐匿于西溪湿地的奢华度假村，中式园林风格")
                        .dangciText("豪华型")
                        .dangciImgUrl("https://img.qunarzz.com/p/hotel/star5.png")
                        .recommendation("西溪湿地最佳度假选择，私密性极佳")
                        .commentDesc("环境优美，服务细致入微，非常适合度假放松")
                        .hotelDetailScheme("qunar://hotel/detail?seq=hotel_003")
                        .collected(true)
                        .build(),
                HotelInfo.builder()
                        .hotelName("全季酒店(杭州西湖店)")
                        .hotelSeq("hotel_004")
                        .score(4.5)
                        .price(HotelInfo.HotelPrice.builder().price(45000).currency("CNY").priceDesc("¥450起").build())
                        .imageUrl("https://img.qunarzz.com/p/hotel/004.jpg")
                        .tagList(Arrays.asList("经济型", "近地铁", "高性价比"))
                        .hotelAddress("杭州市上城区延安路88号")
                        .locationInfo("距西湖步行10分钟")
                        .hotelBriefDesc("位于市中心，交通便利，步行可达西湖")
                        .dangciText("舒适型")
                        .dangciImgUrl("https://img.qunarzz.com/p/hotel/star3.png")
                        .recommendation("经济实惠，位置好，出行方便")
                        .commentDesc("干净整洁，位置绝佳，性价比高")
                        .hotelDetailScheme("qunar://hotel/detail?seq=hotel_004")
                        .collected(false)
                        .build(),
                HotelInfo.builder()
                        .hotelName("杭州洲际酒店")
                        .hotelSeq("hotel_005")
                        .score(4.7)
                        .price(HotelInfo.HotelPrice.builder().price(98000).currency("CNY").priceDesc("¥980起").build())
                        .imageUrl("https://img.qunarzz.com/p/hotel/005.jpg")
                        .tagList(Arrays.asList("商务", "五星级", "钱塘江"))
                        .hotelAddress("杭州市江干区解放东路2号")
                        .locationInfo("钱江新城核心区")
                        .hotelBriefDesc("钱塘江畔的标志性球形建筑，尽揽江景与城市繁华")
                        .dangciText("五星级")
                        .dangciImgUrl("https://img.qunarzz.com/p/hotel/star5.png")
                        .recommendation("商务出行首选，钱塘江景尽收眼底")
                        .commentDesc("建筑独特，江景壮观，早餐丰富")
                        .hotelDetailScheme("qunar://hotel/detail?seq=hotel_005")
                        .collected(false)
                        .build()
        );
    }
}
