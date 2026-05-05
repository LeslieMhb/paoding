package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 统一响应格式
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class JsonV2<T> {

    @JsonProperty("ret")
    private Boolean ret;

    @JsonProperty("errmsg")
    private String errmsg;

    @JsonProperty("data")
    private T data;

    public static <T> JsonV2<T> success(T data) {
        return new JsonV2<>(true, null, data);
    }

    public static <T> JsonV2<T> fail(String errmsg) {
        return new JsonV2<>(false, errmsg, null);
    }
}
