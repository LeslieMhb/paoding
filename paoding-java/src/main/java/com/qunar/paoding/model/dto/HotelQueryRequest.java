package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 酒店查询请求
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HotelQueryRequest {

    /** 目的城市 */
    @JsonProperty("arrCity")
    private String arrCity;

    /** 入住日期, 格式 yyyy-MM-dd */
    @JsonProperty("fromDate")
    private String fromDate;

    /** 离店日期, 格式 yyyy-MM-dd */
    @JsonProperty("toDate")
    private String toDate;

    /** 搜索关键词(酒店名/描述) */
    @JsonProperty("q")
    private String q;

    /** 成人数量 */
    @JsonProperty("adult")
    @Builder.Default
    private Integer adult = 1;

    /** 儿童数量 */
    @JsonProperty("child")
    @Builder.Default
    private Integer child = 0;

    /** 婴儿数量 */
    @JsonProperty("baby")
    @Builder.Default
    private Integer baby = 0;

    /** 最低价格 */
    @JsonProperty("minPrice")
    private Integer minPrice;

    /** 最高价格 */
    @JsonProperty("maxPrice")
    private Integer maxPrice;

    /** 酒店星级 */
    @JsonProperty("level")
    private Integer level;

    /** 排序方式 */
    @JsonProperty("sort")
    private String sort;
}
