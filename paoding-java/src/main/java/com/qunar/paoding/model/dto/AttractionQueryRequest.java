package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 景点/路线查询请求
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AttractionQueryRequest {

    /** 目的地 */
    @JsonProperty("arrival")
    private String arrival;

    /** 出发城市 */
    @JsonProperty("departure")
    private String departure;

    /** 出行开始日期, 格式 yyyy-MM-dd */
    @JsonProperty("startDate")
    private String startDate;

    /** 出行结束日期, 格式 yyyy-MM-dd */
    @JsonProperty("endDate")
    private String endDate;

    /** 出行天数 */
    @JsonProperty("days")
    private Integer days;

    /** 成人数量 */
    @JsonProperty("adultCount")
    @Builder.Default
    private Integer adultCount = 1;

    /** 儿童数量 */
    @JsonProperty("childCount")
    @Builder.Default
    private Integer childCount = 0;

    /** 偏好标签 */
    @JsonProperty("selectTags")
    private List<String> selectTags;

    /** 搜索关键词 */
    @JsonProperty("q")
    private String q;
}
