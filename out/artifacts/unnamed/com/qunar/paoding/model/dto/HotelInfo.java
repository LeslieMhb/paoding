package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 酒店信息
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HotelInfo {

    /** 酒店名称 */
    @JsonProperty("hotelName")
    private String hotelName;

    /** 酒店ID */
    @JsonProperty("hotelSeq")
    private String hotelSeq;

    /** 酒店评分 */
    @JsonProperty("score")
    private Double score;

    /** 酒店价格 */
    @JsonProperty("price")
    private HotelPrice price;

    /** 酒店图片URL */
    @JsonProperty("imageUrl")
    private String imageUrl;

    /** 酒店标签 */
    @JsonProperty("tagList")
    private List<String> tagList;

    /** 酒店地址 */
    @JsonProperty("hotelAddress")
    private String hotelAddress;

    /** 位置信息 */
    @JsonProperty("locationInfo")
    private String locationInfo;

    /** 酒店简介 */
    @JsonProperty("hotelBriefDesc")
    private String hotelBriefDesc;

    /** 档次描述(如: 五星级/豪华型) */
    @JsonProperty("dangciText")
    private String dangciText;

    /** 档次图标URL */
    @JsonProperty("dangciImgUrl")
    private String dangciImgUrl;

    /** 推荐语 */
    @JsonProperty("recommendation")
    private String recommendation;

    /** 评论描述 */
    @JsonProperty("commentDesc")
    private String commentDesc;

    /** 酒店详情页链接 */
    @JsonProperty("hotelDetailScheme")
    private String hotelDetailScheme;

    /** 是否已收藏 */
    @JsonProperty("collected")
    @Builder.Default
    private Boolean collected = false;

    /**
     * 酒店价格信息
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class HotelPrice {

        /** 价格值(分) */
        @JsonProperty("price")
        private Integer price;

        /** 货币单位 */
        @JsonProperty("currency")
        @Builder.Default
        private String currency = "CNY";

        /** 价格描述 */
        @JsonProperty("priceDesc")
        private String priceDesc;
    }
}
