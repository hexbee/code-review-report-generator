from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Literal, Union, ClassVar, Any
from enum import Enum


class Meta(BaseModel):
    commit: str = Field(..., description="Git commit SHA")
    author: str = Field(..., description="Author name")
    email: Optional[EmailStr] = Field(None, description="Author email")
    date: str = Field(..., description="Commit date")


class ChecklistItemType(str, Enum):
    """预定义的35个检查清单项"""
    ITEM_1 = "确保没有使用未初始化的指针或未检查有效性的可选变量"
    ITEM_2 = "验证没有使用已移动的对象"
    ITEM_3 = "防止使用未初始化的变量"
    ITEM_4 = "检查数组和向量的越界访问"
    ITEM_5 = "确保没有数据截断问题（如u32转u8），必要时使用gsl::narrow"
    ITEM_6 = "避免在迭代过程中使用无效迭代器"
    ITEM_7 = "不在基于范围的循环中删除元素"
    ITEM_8 = "确保存储在容器中的迭代器在插入或删除前有效"
    ITEM_9 = "验证lambda中捕获的引用和this在lambda执行时保持有效"
    ITEM_10 = "注册回调时确保对象在回调执行期间保持存活"
    ITEM_11 = "确保多线程环境中共享数据的正确锁定"
    ITEM_12 = "使用适当的锁：必要时使用写锁，避免过度使用写锁"
    ITEM_13 = "验证库函数是否会抛出异常并确保正确处理"
    ITEM_14 = "考虑在传播异常前进行内部异常处理以回滚资源"
    ITEM_15 = "避免直接使用std::get，优先使用std::get_if或带检查的std::visit"
    ITEM_16 = "在循环中修改元素时正确使用auto&"
    ITEM_17 = "验证非const引用返回值的auto&使用"
    ITEM_18 = "避免在引用中忘记&导致意外复制"
    ITEM_19 = "确保新请求的正确并发处理"
    ITEM_20 = "确认状态机正确处理异常事件"
    ITEM_21 = "验证状态退出时正确注销响应消息和停止定时器"
    ITEM_22 = "注册响应消息时设置定时器并在状态机中处理定时器过期"
    ITEM_23 = "避免在状态转换中消息发送成功前提前返回"
    ITEM_24 = "验证空容器的std::all_of、std::any_of、std::none_of结果"
    ITEM_25 = "确认需要时输入容器已排序"
    ITEM_26 = "确保std::copy、std::transform时正确调整大小或使用std::back_inserter"
    ITEM_27 = "防止使用insert或emplace覆盖std::map中的键，使用insert_or_assign代替"
    ITEM_28 = "防止用来自不同目标的消息数据覆盖类成员"
    ITEM_29 = "根据规范验证条件，避免双重否定"
    ITEM_30 = "确保在比较前正确检查IPv4/IPv6存在性"
    ITEM_31 = "鼓励在不同上下文中使用通用函数处理重复逻辑"
    ITEM_32 = "在解引用前验证指针（包括智能指针）和optional的有效性"
    ITEM_33 = "避免直接记录敏感数据"
    ITEM_34 = "确保不记录未初始化/null指针或optional值"
    ITEM_35 = "在打印前正确转换U8变量以避免字符误解"


class ChecklistItem(BaseModel):
    id: int = Field(..., description="Checklist item ID", ge=1, le=35)
    description: ChecklistItemType = Field(..., description="Description of the checklist item")
    passed: bool = Field(..., description="Whether the checklist item passed")
    
    @field_validator('description')
    @classmethod
    def validate_description_id_match(cls, v: ChecklistItemType, info: Any) -> ChecklistItemType:
        """确保description与id匹配"""
        values = info.data
        if 'id' in values:
            item_id = values['id']
            expected_name = f"ITEM_{item_id}"
            # 根据id获取预期的描述
            expected_value = getattr(ChecklistItemType, expected_name, None)
            if v != expected_value:
                raise ValueError(f"ID {item_id} 应该对应描述: {expected_value}")
        return v


class Checklist(BaseModel):
    items: List[ChecklistItem] = Field(
        ..., 
        description="List of checklist items",
        min_items=35,
        max_items=35
    )
    total: Optional[int] = Field(None, description="Total number of checklist items")
    passed: Optional[int] = Field(None, description="Number of passed checklist items")
    
    # 定义固定的检查项数量
    REQUIRED_ITEM_COUNT: ClassVar[int] = 35
    
    @field_validator('items')
    @classmethod
    def validate_item_count(cls, v: List[ChecklistItem]) -> List[ChecklistItem]:
        """验证检查项数量必须是35个"""
        if len(v) != cls.REQUIRED_ITEM_COUNT:
            raise ValueError(f"检查清单必须包含正好{cls.REQUIRED_ITEM_COUNT}个项目，当前数量: {len(v)}")
        
        # 检查是否所有ID从1到35都存在
        ids = {item.id for item in v}
        expected_ids = set(range(1, cls.REQUIRED_ITEM_COUNT + 1))
        if ids != expected_ids:
            missing_ids = expected_ids - ids
            extra_ids = ids - expected_ids
            error_msg = ""
            if missing_ids:
                error_msg += f"缺少ID: {missing_ids} "
            if extra_ids:
                error_msg += f"存在额外ID: {extra_ids}"
            raise ValueError(error_msg)
        
        return v

    def model_post_init(self, __context):
        """
        Calculate total and passed items count if not provided.
        """
        if self.total is None:
            self.total = len(self.items)
        if self.passed is None:
            self.passed = sum(1 for item in self.items if item.passed)


CategoryType = Literal[
    "可维护性", "测试", "设计", "功能", "性能", "安全", 
    "风格", "注释", "错误处理", "日志", "资源管理", "并发", "可扩展性"
]

SeverityType = Literal["critical", "high", "medium", "low"]


class Finding(BaseModel):
    id: str = Field(..., description="Finding ID (e.g., P001)")
    category: CategoryType = Field(..., description="Category of the finding")
    severity: SeverityType = Field(..., description="Severity of the finding")
    location: str = Field(..., description="File location of the finding")
    description: str = Field(..., description="Detailed description of the finding")
    recommendation: str = Field(..., description="Recommendation to fix the issue")
    reference: Union[str, None] = Field("omit", description="Reference code or information")


class CodeReviewReport(BaseModel):
    title: str = Field(..., description="The title of the report")
    meta: Meta = Field(..., description="Metadata about the commit")
    commit_message: str = Field(..., description="The full commit message")
    main_changes: List[str] = Field(..., description="List of main changes in the commit")
    checklist: Checklist = Field(..., description="Code review checklist")
    findings: List[Finding] = Field(
        ..., 
        description="List of findings or issues",
        min_items=3
    )


# 使用示例
def validate_json_file(file_path: str) -> CodeReviewReport:
    """
    Validate a JSON file against the CodeReviewReport model.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        CodeReviewReport: Validated model instance
    """
    import json
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 验证数据并返回模型实例
    return CodeReviewReport.model_validate(data)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <json_file>")
        sys.exit(1)
    
    try:
        report = validate_json_file(sys.argv[1])
        print(f"✅ 验证成功! 报告标题: {report.title}")
        print(f"   检查项: {report.checklist.passed}/{report.checklist.total}")
        print(f"   发现问题: {len(report.findings)}")
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        sys.exit(1) 