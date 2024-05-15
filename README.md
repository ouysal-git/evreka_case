# evreka_case


## To run application in container:

```
docker-compose up -d
```

## GraphQL Example Commands

### Add New Device

```
mutation {
    createDevice(name:"Oguz", ipAddress:"127.0.0.1", port:65432) {
        device {
            name
          	ipAddress
          	port
          	id
        }
        ok
    }
}
```

### Delete Device

```
mutation {
    deleteDevice(id:14) {
        ok
    		message
    }
}
```

### Device List

```
query {
    deviceList {
      name
      id
      ipAddress
      port
    }
}
```

### Device Locations

```
query {
    deviceLocations {
      name
      latitude
      longitude
      timestamp
    }
}
```

### Location History of Device

```
query {
    locationHistory(id: 1) {
      name
      locations {
        latitude
        longitude
        timestamp
      }
    }
}
```
