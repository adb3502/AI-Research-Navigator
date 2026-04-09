from graph.workflow import build_graph

def main():

    background = input("Enter your background: ")

    target = input("Enter target research field: ")

    graph = build_graph()

    result = graph.invoke({
        "background": background,
        "target": target
    })

    print("\n===== Knowledge Plan =====")
    print(result["knowledge_plan"])

    print("\n===== Courses =====")
    print(result["courses"])

    print("\n===== Research Trends =====")
    print(result["trends"])

    print("\n===== Papers =====")
    print(result["recommended_papers"])


if __name__ == "__main__":
    main()