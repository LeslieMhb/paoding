package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 景点信息
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AttractionInfo {

    /** 景点ID */
    @JsonProperty("sightId")
    private String sightId;

    /** 景点名称 */
    @JsonProperty("title")
    private String title;

    /** 景点封面图 */
    @JsonProperty("imageUrl")
    private String imageUrl;

    /** 是否已选中 */
    @JsonProperty("selected")
    @Builder.Default
    private Boolean selected = false;

    /** 景点详情 */
    @JsonProperty("detail")
    private AttractionDetail detail;

    /**
     * 景点详情
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class AttractionDetail {

        /** 标题 */
        @JsonProperty("title")
        private String title;

        /** 副标题 */
        @JsonProperty("subtitle")
        private String subtitle;

        /** 图片列表 */
        @JsonProperty("imageUrlList")
        private List<String> imageUrlList;

        /** 景点描述 */
        @JsonProperty("description")
        private String description;

        /** 贴士列表 */
        @JsonProperty("tips")
        private List<String> tips;
    }
}
