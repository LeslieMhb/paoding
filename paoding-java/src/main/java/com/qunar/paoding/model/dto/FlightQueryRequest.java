package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 机票查询请求
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class FlightQueryRequest {

    /** 出发城市 */
    @JsonProperty("depCity")
    private String depCity;

    /** 到达城市 */
    @JsonProperty("arrCity")
    private String arrCity;

    /** 出发日期, 格式 yyyy-MM-dd */
    @JsonProperty("goDate")
    private String goDate;

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
}
