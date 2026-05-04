package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 交通搜索结果(含机票和火车票)
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TransportListResult {

    /** 机票列表 */
    @JsonProperty("flightList")
    private List<FlightInfo> flightList;

    /** 火车票列表 */
    @JsonProperty("trainList")
    private List<TrainInfo> trainList;

    /** 推荐标题 */
    @JsonProperty("recommendTitle")
    private String recommendTitle;

    /** 推荐副标题 */
    @JsonProperty("recommendSubTitle")
    private String recommendSubTitle;

    /** 更多机票链接 */
    @JsonProperty("recommendMoreFlightScheme")
    private String recommendMoreFlightScheme;

    /** 更多火车票链接 */
    @JsonProperty("recommendMoreTrainScheme")
    private String recommendMoreTrainScheme;
}
