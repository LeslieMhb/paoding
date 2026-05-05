package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 路线规划结果
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RoutePlanResult {

    /** 路线标题 */
    @JsonProperty("title")
    private String title;

    /** 天数 */
    @JsonProperty("days")
    private Integer days;

    /** 每日路线列表 */
    @JsonProperty("dayRouteList")
    private List<DayRoute> dayRouteList;

    /**
     * 单日路线
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class DayRoute {

        /** 第几天(从1开始) */
        @JsonProperty("day")
        private Integer day;

        /** 当日主题 */
        @JsonProperty("theme")
        private String theme;

        /** 路线描述(如: A -> B -> C) */
        @JsonProperty("routeText")
        private String routeText;

        /** 亮点/注意事项 */
        @JsonProperty("highlights")
        private String highlights;

        /** 当日详细描述 */
        @JsonProperty("fullDesc")
        private String fullDesc;

        /** 当日景点列表 */
        @JsonProperty("spots")
        private List<PoiSpot> spots;
    }

    /**
     * 景点位置信息
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class PoiSpot {

        /** 景点名称 */
        @JsonProperty("name")
        private String name;

        /** 所在城市 */
        @JsonProperty("city")
        private String city;

        /** 所在省份 */
        @JsonProperty("province")
        private String province;

        /** 所在国家 */
        @JsonProperty("country")
        @Builder.Default
        private String country = "中国";

        /** 景点描述 */
        @JsonProperty("description")
        private String description;
    }
}
