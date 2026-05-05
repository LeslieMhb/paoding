package com.qunar.paoding.config;

import com.qunar.paoding.model.dto.JsonV2;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public JsonV2<Void> handleException(Exception e) {
        log.error("Unhandled exception: ", e);
        return JsonV2.fail("服务内部错误: " + e.getMessage());
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public JsonV2<Void> handleIllegalArgument(IllegalArgumentException e) {
        log.warn("Invalid argument: {}", e.getMessage());
        return JsonV2.fail("参数错误: " + e.getMessage());
    }
}
